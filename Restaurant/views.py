# from django.shortcuts import render, get_object_or_404
# from django.http import JsonResponse
# from django.db.models import Q
# from django.contrib.auth.decorators import login_required
# from .models import Restaurant, MenuItem, FoodCategory, CustomizationOption
# from django.conf import settings
# import math

# def calculate_distance(lat1, lon1, lat2, lon2):
#     # Haversine formula to calculate distance between two points
#     R = 6371  # Radius of Earth in km
#     dLat = math.radians(lat2 - lat1)
#     dLon = math.radians(lon2 - lon1)
#     a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
#     c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
#     distance = R * c
#     return distance

# def search_restaurant(request):
#     query = request.GET.get('q', '')
#     category = request.GET.get('category', '')
#     lat = request.GET.get('lat')
#     lon = request.GET.get('lon')
    
#     restaurants = Restaurant.objects.filter(is_active=True)
    
#     # Apply search filter
#     if query:
#         restaurants = restaurants.filter(
#             Q(name__icontains=query) | 
#             Q(cuisine_type__icontains=query) |
#             Q(menu_items__name__icontains=query)
#         ).distinct()
    
#     # Apply category filter
#     if category:
#         restaurants = restaurants.filter(cuisine_type=category)
    
#     # Calculate distance if coordinates provided
#     restaurant_list = []
#     if lat and lon:
#         try:
#             user_lat = float(lat)
#             user_lon = float(lon)
            
#             for rest in restaurants:
#                 distance = calculate_distance(user_lat, user_lon, rest.latitude, rest.longitude)
#                 if distance <= settings.MAX_DELIVERY_DISTANCE:
#                     restaurant_list.append({
#                         'id': rest.id,
#                         'name': rest.name,
#                         'cuisine_type': rest.cuisine_type,
#                         'rating': rest.rating,
#                         'distance': round(distance, 2)
#                     })
            
#             # Sort by distance
#             restaurant_list.sort(key=lambda x: x['distance'])
#         except (ValueError, TypeError):
#             pass
    
#     return JsonResponse({'restaurants': restaurant_list})

# def view_restaurant(request, restaurant_id):
#     restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_active=True)
#     menu_items = MenuItem.objects.filter(restaurant=restaurant, is_available=True)
    
#     # Group menu items by category
#     categories = {}
#     for item in menu_items:
#         category_name = item.category.name if item.category else "Other"
#         if category_name not in categories:
#             categories[category_name] = []
        
#         # Get customization options
#         customization_options = []
#         for option in CustomizationOption.objects.filter(menu_item=item):
#             choices = option.choices.all().values('id', 'name', 'additional_price')
#             customization_options.append({
#                 'id': option.id,
#                 'name': option.name,
#                 'type': option.option_type,
#                 'required': option.is_required,
#                 'choices': list(choices)
#             })
        
#         categories[category_name].append({
#             'id': item.id,
#             'name': item.name,
#             'description': item.description,
#             'price': float(item.price),
#             'image': item.image.url if item.image else None,
#             'customization_options': customization_options
#         })
    
#     response_data = {
#         'id': restaurant.id,
#         'name': restaurant.name,
#         'description': restaurant.description,
#         'cuisine_type': restaurant.cuisine_type,
#         'address': restaurant.address,
#         'rating': restaurant.rating,
#         'total_ratings': restaurant.total_ratings,
#         'categories': categories
#     }
    
#     return JsonResponse(response_data)

# @login_required
# def manage_menu(request, restaurant_id):
#     # Implementation for restaurant owners to manage their menu
#     pass