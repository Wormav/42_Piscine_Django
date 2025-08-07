from django.shortcuts import render

# Create your views here.
def color_shades(request):
    colors = []

    for i in range(50):
        # Calculate intensity
        intensity = int((i / 50) * 255)

        # Create nuances
        black_shade = f"rgb({intensity}, {intensity}, {intensity})"
        red_shade = f"rgb(255, {255-intensity}, {255-intensity})"
        blue_shade = f"rgb({255-intensity}, {255-intensity}, 255)"
        green_shade = f"rgb({255-intensity}, 255, {255-intensity})"

        colors.append({
            'black': black_shade,
            'red': red_shade,
            'blue': blue_shade,
            'green': green_shade
        })

    return render(request, 'shades.html', {'colors': colors})
