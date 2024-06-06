from django.shortcuts import render,redirect
from .forms import createUser,LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from .models import Record
import requests
import pandas as pd
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML
from django.http import HttpResponse, JsonResponse
import os
from django.conf import settings
import jinja2
import pdfkit
from datetime import datetime




def home(request):
    
    return render(request,'webapp/index.html')


#register

def register(request):
    form=createUser()

    if request.method == "POST" :
        form = createUser(request.POST)

        if form.is_valid():
            form.save()

            return redirect('login')
    
    context={'form':form}
    return render(request,'webapp/register.html',context=context)

#login

def login(request):
    form =LoginForm()
    if request.method=='POST':
        form =LoginForm(request,data=request.POST)
        if form.is_valid():
            username=request.POST.get('username')
            password=request.POST.get('password')

            user=authenticate(request,username=username,password=password)
            if user is not None:
                auth.login(request,user)
                return redirect('dashboard')
    context= {'loginform':form}
    return render(request,'webapp/login.html',context=context)

#dashboard
@login_required(login_url='login')
def dashboard(request):
    # my_records=Record.objects.all()
    # context={'records':my_records}


    url = "https://fake-coffee-api.vercel.app/api"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(data)  # Print the data for debugging purposes
        return render(request, 'webapp/dashboard.html', {'data': data})
    else:
        error_message = 'Failed to fetch data. Status code: {}'.format(response.status_code)
        print(error_message)  # Print the error message for debugging purposes
        return render(request, 'webapp/dashboard.html', {'error': error_message})
    # return render(request,'webapp/dashboard.html',context=data)

import pdfkit
import base64
from django.http import JsonResponse


    

@csrf_exempt
async def checkout(request):
    if request.method == 'POST':
        cart_data = request.POST.get('cart_data')
        # username = request.POST.get('username')
        # phone = request.POST.get('phone')
        username ='admin'
        phone = '9726626222'
        invoice_date = datetime.today().strftime("%d,%b,%y")


        # Parse the cart_data string and create a DataFrame
        cart_items = pd.read_json(cart_data)
        
        # Convert DataFrame to a list of dictionaries
        cart_data_list = cart_items.to_dict(orient='records')
        for item in cart_data_list:
            item['price'] = float(item['price'].replace('$', ''))
            item['subtotal'] = item['price'] * item['count']
        total = sum(item['subtotal'] for item in cart_data_list)

        context = {
        'amount':total,
        'total_amount':total 

       }
        response = render(request, 'webapp/cart_esewa.html',context)
        response_content = "success"
        # return render(request, 'webapp/cart_esewa.html', context)
        if response_content == "success":

            # Render the checkout template with the processed data
            html_content = render(request, 'webapp/checkout.html', {'data': cart_data_list, 'total': total,'username':username,'phone':phone,'invoice_date':invoice_date})
            
            # Convert HTML content to PDF
            pdf_content = pdfkit.from_string(html_content.content.decode(), False)
            
            # Save the PDF content to a file if conversion is successful
            if pdf_content:
                pdf_filename = 'receipt.pdf'
                with open(pdf_filename, 'wb') as pdf_file:
                    pdf_file.write(pdf_content)
                # Encode PDF content in base64
                pdf_base64 = base64.b64encode(pdf_content).decode('utf-8')
                # Return JSON response with HTML and base64-encoded PDF content
                return JsonResponse({'html': html_content.content.decode()})
            else:
                # If conversion fails, return an error response
                return JsonResponse({'error': 'PDF conversion failed'}, status=500)
    else:
        return redirect('dashboard')



#logout

def user_logout(request):
    auth.logout(request)
    return redirect("login")