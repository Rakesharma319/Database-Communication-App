# def Current_User(Email_id):
#   d2=Email_id.split("@",1)
#   return "Hello "+ d2[0]


def Current_User(string,delimiters):
  for delimiter in delimiters:
     string = " ".join(string.split(delimiter))
 
  result = string.split()
  result=result[0]
 
  return result
