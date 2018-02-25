from word_forms.word_forms import get_word_forms

outdic ={}
outdic = get_word_forms("secret")
print(outdic)
print("noun", list(outdic.get('n')))
print("adj",list(outdic.get('a')))
print("adv",list(outdic.get('r')))
print("verb",list(outdic.get('v')))
