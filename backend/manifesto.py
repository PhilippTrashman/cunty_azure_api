
def get_manifesto():
    with open('./backend/manifesto.txt', 'r') as f:
        return f.read()