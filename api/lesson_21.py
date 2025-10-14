# def format_name(first,last):
#    full = first.title() + " " + last.title()
#    return full

# print(format_name("John","Doe"))

def format_name(first : str,last : str):
    full = first.title() + " " + last.title()
    return full

print(format_name("John","Doe"))

def get_items(item_a:str,item_b:int,item_c:float,item_d:bool,item_e:bytes):
    return item_a,item_b,item_c,item_d,item_e

print(get_items('suela','17','7.77','True'))