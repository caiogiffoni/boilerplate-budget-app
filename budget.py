import math

class Category:

  def __init__(self, cat: str):
    self.category = cat
    self.ledger: list = []
    self.balance = 0

  def deposit(self, amount: float, description: str = ''):
    self.balance += amount
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount: int, description: str = ''):
    if not self.check_funds(amount):
      return False
    self.balance -= amount
    self.ledger.append({"amount": -amount, "description": description})
    return True

  def get_balance(self):
    return self.balance

  def transfer(self, amount: float, obj):
    if not self.check_funds(amount):
      return False
    self.withdraw(amount, f"Transfer to {obj.category}")
    obj.deposit(amount, f"Transfer from {self.category}")
    return True

  def check_funds(self, amount: float):
    return True if self.balance >= amount else False

  def __str__(self):
    returnStr: str = ''
    starts = int((30 - len(self.category)) / 2)
    returnStr += f"{'*'*starts}{self.category}{'*'*starts}\n"
    for transaction in self.ledger:
      charac = len(transaction["description"]) + len(str(
        transaction["amount"]))
      charac += 3 if transaction["amount"] == round(transaction["amount"]) else 0
      if charac > 30:
        indexDescr = 30 - len(str(transaction["amount"])) - 1
        indexDescr -= 3 if transaction["amount"] == round(transaction["amount"]) else 0
        returnStr += f'{transaction["description"][0:indexDescr]}{" "}{transaction["amount"]:.2f}\n'
      else:
        returnStr += f'{transaction["description"]}{" "*(30-charac)}{transaction["amount"]:.2f}\n'
    returnStr += f'Total: {sum([t["amount"] for t in self.ledger])}'
    return returnStr


def create_spend_chart(categories: Category):
  spentValues = {}
  spentPerc = {}
  for cat in categories:
    spentValues[cat.category] = sum(
      [trans['amount'] for trans in cat.ledger if trans['amount'] < 0])
  totalSpent = sum([spentValues[key] for key in spentValues])
  for key in spentValues:
    spentPerc[key] = math.floor((spentValues[key]) * 10 / totalSpent) * 10
  returnStr = 'Percentage spent by category\n'
  for x in reversed(range(11)):
    number = f'{" "*(3-(len(str(x*10))))}{x*10}'
    spaces: str = ''
    for cat in spentPerc:
      spaces += f'{" o "}' if spentPerc[cat] >= x*10 else f'{" "*3}'
    returnStr += f'{number}|{spaces} \n'
  biggerWord =  max([len(cat.category) for cat in categories])
  returnStr += f'    {"-"*(len(categories)*3+1)}\n'
  for index in range(biggerWord):
    returnStr += '    '
    for cat in categories:
      returnStr += f' {cat.category[index]} 'if len(cat.category) > index else '   '
    returnStr += ' \n'
  return f'{returnStr[:-2]} '
