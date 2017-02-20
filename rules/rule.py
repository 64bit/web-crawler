class Rule(object):
  
  def __init__(self):
    pass

  def matches(self, url_parse_result):
    # derived classes will implement this
    return True
