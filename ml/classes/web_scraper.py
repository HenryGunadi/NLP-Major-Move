from abc import ABC, abstractmethod
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

class WebScraper(ABC):
  def __init__(self, base_url):
    self.base_url = base_url

  @abstractmethod
  def fetch(self, url, **kwargs):
    """Fetch page content"""
    pass

  @abstractmethod
  def parse(self, html):
    """Parse fetched HTML into structured data"""
    pass

  def run(self):
    """Run the whole process"""
    pass

class InvestingComScraper(WebScraper):
  def fetch(self, url):
    try:
      req = Request(
        url,
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://id.investing.com/",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }
      )

      page = urlopen(req)
      final_url = page.geturl()

      # reached the maximum page index
      if final_url != url:
        print("Reached the maximum page index — stopping.")
        return

      html = page.read().decode("utf-8")
      print(f"Fetch Success ({url})")
      return html
    except Exception as e:
      print(f"Error fecthing html ({url}) : ", e)
      raise

  def parse(self, html):
    try:
      pass
    except Exception as e:
      print(f"Error parsing html : ", e)
      raise

  def run(self):
    page_index = 1

    while True:
      try:
        url = f"{self.base_url}/{page_index}"

        html = self.fetch(url=url)

        if not html:
          print("Maximum index has been reached.")
          break

        processed_data = self.parse(html=html)
          

      except Exception as e:
        print(f"Error collecting data : ", e)
        break
