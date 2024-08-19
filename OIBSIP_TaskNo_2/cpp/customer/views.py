from django.shortcuts import render

# Create your views here.
def index(request):
    if request.method == "POST":
        brand = request.POST.get('brand', '')
        model_name = request.POST.get('model', '')  
        year = request.POST.get('year', '')
        fuel_type = request.POST.get('fuel_type', '')
        transmission = request.POST.get('transmission', '')

        # Check for empty inputs
        if not (brand and model_name and year and fuel_type and transmission):
            return render(request, "predict.html", {
                "error": "Please provide all required input values."
            })

        # Convert year to float
        try:
            year = float(year)
        except ValueError:
            return render(request, "predict.html", {
                "error": "Please enter a valid numeric value for the year."
            })
        
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LinearRegression
        from sklearn.preprocessing import LabelEncoder


        # Load the predictset
        df = pd.read_csv(r"static\dataset\car_prices.csv")
        print(df.isnull().sum())
        df.dropna(inplace=True)


        # Initialize LabelEncoders
        le_brand = LabelEncoder()
        le_model_name = LabelEncoder()  
        le_fuel_type = LabelEncoder()
        le_transmission = LabelEncoder()


        #Fit and transform the predictset's categorical columns
        df['brand'] = le_brand.fit_transform(df['brand'])
        df['model'] = le_model_name.fit_transform(df['model'])  
        df['fuel_type'] = le_fuel_type.fit_transform(df['fuel_type'])
        df['transmission'] = le_transmission.fit_transform(df['transmission'])

    
        x = df.drop(["mileage", "horsepower", "doors", "price"], axis=1)
        y = df["price"]

        model = LinearRegression()
        model.fit(x, y)


        #Prepare input for prediction
        brand_encoded = le_brand.transform([brand])[0]
        model_name_encoded = le_model_name.transform([model_name])[0] 
        fuel_type_encoded = le_fuel_type.transform([fuel_type])[0]
        transmission_encoded = le_transmission.transform([transmission])[0]

        pred_input = np.array([[brand_encoded, model_name_encoded, year, fuel_type_encoded, transmission_encoded]])
        
        #prediction
        try:
            pred_outcome = model.predict(pred_input)
            prediction = pred_outcome[0]
        except Exception as e:
            return render(request, "index.html", {
                "error": f"An error occurred during prediction: {str(e)}"
            })


        return render(request, "predict.html", {
            "brand": brand,
            "model": model_name,  
            "year": year,
            "fuel_type": fuel_type,
            "transmission": transmission,
            "prediction": prediction
        })
    else:
        return render(request, "index.html")

          
def predict(request):
    return render(request, "predict.html")