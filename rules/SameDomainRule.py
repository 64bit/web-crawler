from rule import Rule

class SameDomainRule(Rule):
  def __init__(self, host):
    self.host = host

  def matches(self, url_parse_result):
    if url_parse_result.netloc == self.host:
      return True 
    return False
