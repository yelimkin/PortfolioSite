from django.shortcuts import render
from django.views.generic import TemplateView
import pickle
import numpy as np


# Create your views here.
class IrisHome(TemplateView):
    template_name = 'ml_deploy/iris_home.html'

def irisPredict(request):
    if request.method == 'POST':
        form = request.POST

        print(form)
        print(len(form))
        print(form['a'].isdigit())
        print(len(form) > 4 and form['a'].isdigit() and form['b'].isdigit() and form['c'].isdigit() and form['d'].isdigit())

        if(len(form) > 4 and form['a'].isdigit() and form['b'].isdigit() and form['c'].isdigit() and form['d'].isdigit()):
            model = pickle.load(open('static/models/iris_model_svc.pkl', 'rb'))
            data1 = float(form['a'])
            data2 = float(form['b'])
            data3 = float(form['c'])
            data4 = float(form['d'])
            arr = np.array([[data1, data2, data3, data4]])
            pred = model.predict(arr)
            context = {'pred_result' : pred}
        else:
            context = {'warning' : "값을 모두 숫자로 입력하세요. "}

        return render(request, 'ml_deploy/iris_predict.html', context)