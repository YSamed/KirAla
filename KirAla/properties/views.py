from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Property ,PropertyDetails 
from .forms import PropertyForm, PropertyDetailsForm 


# Create your views here.
@login_required
def property_list(request):
    user = request.user
    all_properties = Property.objects.filter(owner=user, is_deleted=False)
    rented_properties = Property.objects.filter(owner=user, is_rented=True, is_deleted=False)
    vacant_properties = Property.objects.filter(owner=user, is_rented=False, is_deleted=False)

    context = {
        'all_properties': all_properties,
        'rented_properties': rented_properties,
        'vacant_properties': vacant_properties,
    }

    return render(request, 'properties/property_list.html', context)



@login_required
def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    return render(request, 'properties/property_detail.html', {'property': property})






@login_required
def property_create(request):
    property_form = PropertyForm(request.POST or None)
    details_form = PropertyDetailsForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if 'next' in request.POST:
            if property_form.is_valid():
                # Save property form data to session
                request.session['property_form_data'] = request.POST
                return redirect('properties:property_create_step2')
        elif 'submit' in request.POST:
            if property_form.is_valid() and details_form.is_valid():
                property = property_form.save(commit=False)
                property.owner = request.user
                property.save()

                details = details_form.save(commit=False)
                details.property = property
                details.save()

                return redirect('properties:property_detail', pk=property.pk)

    context = {
        'property_form': property_form,
        'details_form': details_form,
    }
    return render(request, 'properties/property_create_1.html', context)

@login_required
def property_create_step2(request):
    if 'property_form_data' not in request.session:
        return redirect('properties:property_create')

    property_form = PropertyForm(request.session['property_form_data'])
    details_form = PropertyDetailsForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and 'submit' in request.POST:
        if property_form.is_valid() and details_form.is_valid():
            property = property_form.save(commit=False)
            property.owner = request.user
            property.save()

            details = details_form.save(commit=False)
            details.property = property
            details.save()

            del request.session['property_form_data']  

            return redirect('properties:property_detail', pk=property.pk)

    context = {
        'property_form': property_form,
        'details_form': details_form,
    }
    return render(request, 'properties/property_create_2.html', context)





@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        property.soft_delete() 
        return redirect('properties:property_list')
    
    return render(request, 'properties/property_confirm_delete.html', {'property': property})




@login_required
def property_update_step1(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            return redirect('properties:property_update_step2', pk=pk)
    else:
        form = PropertyForm(instance=property)
    
    context = {
        'form': form,
        'property': property,
    }
    return render(request, 'properties/property_update_step1.html', context)

@login_required
def property_update_step2(request, pk):
    property = get_object_or_404(Property, pk=pk)
    property_details = property.details  

    if request.method == 'POST':
        details_form = PropertyDetailsForm(request.POST, instance=property_details)
        if details_form.is_valid():
            details_form.save()
            return redirect('properties:property_detail', pk=pk)
    else:
        details_form = PropertyDetailsForm(instance=property_details)
    
    context = {
        'details_form': details_form,
        'property': property,
    }
    return render(request, 'properties/property_update_step2.html', context)
