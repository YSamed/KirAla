from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.contrib import messages
from .models import Property, PropertyImage ,PropertyDetails
from .forms import PropertyForm, PropertyDetailsForm, PropertyImageForm


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


#YENİ EKLEME
@login_required
def property_create_step1(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = request.user  
            property_instance.save()

            request.session['new_property'] = property_instance.id  
            return redirect('properties:property_create_step2') 
    else:
        form = PropertyForm()

    context = {
        'form': form,
    }
    return render(request, 'properties/property_create_step1.html', context)

@login_required
def property_create_step2(request):
    property_id = request.session.get('new_property')
    property_instance = get_object_or_404(Property, id=property_id)
    
    try:
        property_details = property_instance.details
    except PropertyDetails.DoesNotExist:
        property_details = None

    if request.method == 'POST':
        if property_details:
            details_form = PropertyDetailsForm(request.POST, instance=property_details)
        else:
            details_form = PropertyDetailsForm(request.POST)
        
        image_form = PropertyImageForm(request.POST, request.FILES)

        if details_form.is_valid() and image_form.is_valid():
            if not property_details:
                details_instance = details_form.save(commit=False)
                details_instance.property = property_instance
                details_instance.save()
            else:
                details_instance = details_form.save()
            
            image_instance = image_form.save(commit=False)
            image_instance.property_details = details_instance
            image_instance.save()

            del request.session['new_property']
            messages.success(request, 'Property has been created successfully!')
            return redirect('properties:property_list') 
    else:
        if property_details:
            details_form = PropertyDetailsForm(instance=property_details)
        else:
            details_form = PropertyDetailsForm()

        image_form = PropertyImageForm()

    context = {
        'details_form': details_form,
        'image_form': image_form,
    }
    return render(request, 'properties/property_create_step2.html', context)


@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        property.soft_delete()
        messages.error(request, 'Property has been deleted successfully!')
        return redirect('properties:property_list')
    
    return render(request, 'properties/property_confirm_delete.html', {'property': property})


#GÜNCELLEME
@login_required
def property_update_step1(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property information has been updated successfully!')
            return redirect('properties:property_update_step2', pk=pk)
        else:
            messages.error(request, 'Form submission failed. Please correct the errors.')
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
    ImageFormSet = modelformset_factory(PropertyImage, form=PropertyImageForm, extra=3)

    if request.method == 'POST':
        details_form = PropertyDetailsForm(request.POST, instance=property_details)
        formset = ImageFormSet(request.POST, request.FILES, queryset=PropertyImage.objects.filter(property_details=property_details))

        if details_form.is_valid() and formset.is_valid():
            details_form.save()
            for form in formset:
                if form.cleaned_data.get('image'):
                    image_instance = form.save(commit=False)
                    image_instance.property_details = property_details
                    image_instance.save()
            messages.success(request, 'Property details have been updated successfully!')
            return redirect('properties:property_detail', pk=pk)
        else:
            messages.error(request, 'Form submission failed. Please correct the errors.')
    else:
        details_form = PropertyDetailsForm(instance=property_details)
        formset = ImageFormSet(queryset=PropertyImage.objects.filter(property_details=property_details))
    
    context = {
        'details_form': details_form,
        'formset': formset,
        'property': property,
    }
    return render(request, 'properties/property_update_step2.html', context)