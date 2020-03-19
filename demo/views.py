from django.shortcuts import render
import copy

# Create your views here.
def home(request):
	context = {}
	if request.method=='GET':
		context['display']='0'
	elif request.method=="POST":
		extract(request.POST, context)
		interpret(request.POST, context)
	return render(request, 'calculator/calculator.html',context)

def extract(post, context):
	for item in post:
		context[item] = copy.deepcopy(post[item])

def interpret(post, context):
	ops = {'+','-','*','/'}
	nums = {str(i) for i in range(10)}

	if post['key'] in ops:

		# change operator
		if post['lastPressed'] in ops or post['lastPressed'] == '=':
			context['storedOp'] = post['key']

		# evaluate math, update screen
		else:
			evaluate(post, context)
			context['storedOp'] = post['key']
			context['storedNum'] = context['display']

	elif post['key'] in nums:
		if post['lastPressed'] in ops or context['display'] == '0': 
			context['display'] = post['key']
		else:
			context['display'] = context['display'] + post['key']

	elif post['key'] == '=':
		if post['lastPressed'] not in ops:
			evaluate(post, context)
			context['storedNum'] = context['display']
			context['storedOp'] = ''
	context['lastPressed'] = post['key']


def evaluate(post,context):
	if not post['storedOp']: return
	if post['storedOp']=='/' and post['display']=='0': return
	print('***' + context['storedNum'] + context['storedOp'] + post['display'])
	context['display'] = eval(context['storedNum'] + context['storedOp'] + context['display'])
