import torch
import torch.nn as nn
from transformers import (
    BertModel,
    BertPreTrainedModel,
    BertTokenizer
)

class FocalLoss(nn.Module):
    def __init__(self, alpha=None, gamma=2.0, label_smoothing=0.0, reduction="mean"):
        super().__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.label_smoothing = label_smoothing
        self.reduction = reduction

    def forward(self, inputs, targets):
        num_classes = inputs.size(-1)
        
        if self.label_smoothing > 0:
            # Label smoothing
            targets_one_hot = torch.nn.functional.one_hot(targets, num_classes).float()
            targets_one_hot = targets_one_hot * (1 - self.label_smoothing) + \
                             self.label_smoothing / num_classes

            log_probs = torch.nn.functional.log_softmax(inputs, dim=-1)
            ce_loss = -(targets_one_hot * log_probs).sum(dim=-1)
        else:
            # Standard cross entropy
            ce_loss = torch.nn.functional.cross_entropy(inputs, targets, weight=self.alpha, reduction='none')

        pt = torch.exp(-ce_loss)
        focal_loss = (1 - pt) ** self.gamma * ce_loss
        
        if self.reduction == "mean":
            return focal_loss.mean()
        elif self.reduction == "sum":
            return focal_loss.sum()
        return focal_loss

class MultiTaskFinBert(BertPreTrainedModel):
    def __init__(self, config, importance_weights=None, sentiment_weights=None):
        super().__init__(config)
        self.num_sent_labels = getattr(config, "num_sent_labels", 3)
        self.num_imp_labels = getattr(config, "num_imp_labels", 2)

        # Match the checkpoint's attribute name: finBert (not bert)
        self.finBert = BertModel(config)

        # Shared layer - matches training code
        self.shared_layer = nn.Sequential(
            nn.Linear(config.hidden_size, 768),
            nn.LayerNorm(768),
            nn.GELU(),
            nn.Dropout(0.2)
        )

        # Sentiment pathway - matches training code exactly
        self.sent_proj1 = nn.Linear(768, 512)
        self.sent_norm1 = nn.LayerNorm(512)
        self.sent_dropout1 = nn.Dropout(0.3)

        self.sent_proj2 = nn.Linear(512, 512)
        self.sent_norm2 = nn.LayerNorm(512)
        self.sent_dropout2 = nn.Dropout(0.3)

        self.sent_proj3 = nn.Linear(512, 256)
        self.sent_norm3 = nn.LayerNorm(256)
        self.sent_dropout3 = nn.Dropout(0.2)

        self.sent_out = nn.Linear(256, self.num_sent_labels)

        # Importance pathway - matches training code exactly
        self.imp_proj1 = nn.Linear(768, 512)
        self.imp_norm1 = nn.LayerNorm(512)
        self.imp_dropout1 = nn.Dropout(0.3)

        self.imp_proj2 = nn.Linear(512, 256)
        self.imp_norm2 = nn.LayerNorm(256)
        self.imp_dropout2 = nn.Dropout(0.3)

        self.imp_out = nn.Linear(256, self.num_imp_labels)

        # Loss functions (not used during inference but needed for loading)
        self.sentiment_loss_fn = FocalLoss(alpha=sentiment_weights, gamma=2.0)
        self.importance_loss_fn = FocalLoss(alpha=importance_weights, gamma=2.5)

        self.post_init()

    def forward(
        self,
        input_ids,
        attention_mask=None,
        token_type_ids=None,
        sentiment=None,
        importance=None
    ):
        outputs = self.finBert(
            input_ids=input_ids,
            attention_mask=attention_mask,
            token_type_ids=token_type_ids
        )

        pooled_output = outputs[1]  # Use pooler output

        # Shared representation
        shared_repr = self.shared_layer(pooled_output)

        # Sentiment pathway with residual connection
        sent_h1 = self.sent_dropout1(torch.nn.functional.gelu(self.sent_norm1(self.sent_proj1(shared_repr))))
        sent_h2 = self.sent_dropout2(torch.nn.functional.gelu(self.sent_norm2(self.sent_proj2(sent_h1))))
        sent_h2 = sent_h2 + sent_h1  # Residual connection
        sent_h3 = self.sent_dropout3(torch.nn.functional.gelu(self.sent_norm3(self.sent_proj3(sent_h2))))
        logits_sent = self.sent_out(sent_h3)

        # Importance pathway
        imp_h1 = self.imp_dropout1(torch.nn.functional.gelu(self.imp_norm1(self.imp_proj1(shared_repr))))
        imp_h2 = self.imp_dropout2(torch.nn.functional.gelu(self.imp_norm2(self.imp_proj2(imp_h1))))
        logits_imp = self.imp_out(imp_h2)

        # Return only logits during inference
        if sentiment is None or importance is None:
            return logits_sent, logits_imp

        # Training mode with loss calculation
        loss_sent = self.sentiment_loss_fn(logits_sent, sentiment)
        loss_imp = self.importance_loss_fn(logits_imp, importance)
        loss = 1.5 * loss_sent + 2.0 * loss_imp

        return loss, logits_sent, logits_imp