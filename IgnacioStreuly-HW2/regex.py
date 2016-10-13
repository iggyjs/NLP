#regex patterns
FULL_PATTERN_DOLLARS = re.compile('|'.join([
  r'[\$][\d{1,3}]\,\d{1,3}\,\d{1,3}', # $1,000,000
  r'[\$][\d{1,3}]\,\d{1,3}\.\d{1,2}', # $100,000.00, $10,000.00
  r'[\$][\d{1,5}]\.\d{1,2}', # $10000.00
  r'[\$](\d+\.\d{1,2})',  # $1.00
  r'[\$][\d{1,3}]\,\d{1,3}', #$100,000, $10,000, 1,000
  r'billion|billions',
  r'trillion|trillions',
  r'million|millions'
]), re.IGNORECASE)

FULL_PATTERN_PHONE = re.compile('|'.join([
  r'\(\d{3}\)[\s]\d{3}[\s-]\d{4}', # (123) 123-1234
  r'\(\d{3}\)[-]\d{3}[\s-]\d{4}', # (123)-123-1234
  r'\d{3}[-]\d{3}[\s-]\d{4}' # 123-123-1234
]), re.IGNORECASE)
