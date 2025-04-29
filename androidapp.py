import flet as ft
import joblib
import numpy as np

# Load your saved model
model = joblib.load(open('heart-disease-model.pkl', 'rb'))

def main(page: ft.Page):
    page.title = "Heart Disease Predictor"
    page.window_width = 400
    page.window_height = 750
    page.bgcolor = ft.Colors.LIGHT_BLUE_50  # Updated Colors enum
    page.scroll = "auto"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Title Text with a Container for margin
    title = ft.Container(
        content=ft.Text(
            value="💓 Heart Disease Predictor",
            size=30,
            weight="bold",
            color=ft.Colors.PINK,  # Updated Colors enum
            text_align="center"
        ),
        margin=ft.margin.only(top=20)
    )

    # Form Fields with padding using Container
    age = ft.Container(
        content=ft.TextField(label="Age", width=300),
        padding=ft.padding.all(8)
    )
    sex = ft.Container(
        content=ft.Dropdown(label="Sex", options=[ft.dropdown.Option("Male"), ft.dropdown.Option("Female")], width=300),
        padding=ft.padding.all(8)
    )
    chest_pain = ft.Container(
        content=ft.TextField(label="Chest Pain Type", width=300),
        padding=ft.padding.all(8)
    )
    blood_pressure = ft.Container(
        content=ft.TextField(label="Resting Blood Pressure", width=300),
        padding=ft.padding.all(8)
    )
    cholesterol = ft.Container(
        content=ft.TextField(label="Cholesterol", width=300),
        padding=ft.padding.all(8)
    )
    fasting_bs = ft.Container(
        content=ft.TextField(label="Fasting Blood Sugar > 120 mg/dl (1 = true; 0 = false)", width=300),
        padding=ft.padding.all(8)
    )
    rest_ecg = ft.Container(
        content=ft.TextField(label="Resting ECG (0,1,2)", width=300),
        padding=ft.padding.all(8)
    )
    max_hr = ft.Container(
        content=ft.TextField(label="Max Heart Rate Achieved", width=300),
        padding=ft.padding.all(8)
    )
    exercise_angina = ft.Container(
        content=ft.Dropdown(label="Exercise Induced Angina", options=[ft.dropdown.Option("Yes"), ft.dropdown.Option("No")], width=300),
        padding=ft.padding.all(8)
    )
    oldpeak = ft.Container(
        content=ft.TextField(label="Oldpeak", width=300),
        padding=ft.padding.all(8)
    )
    slope = ft.Container(
        content=ft.TextField(label="Slope (0,1,2)", width=300),
        padding=ft.padding.all(8)
    )
    ca = ft.Container(
        content=ft.TextField(label="Number of major vessels (0-3)", width=300),
        padding=ft.padding.all(8)
    )
    thal = ft.Container(
        content=ft.TextField(label="Thal (1 = normal; 2 = fixed defect; 3 = reversible defect)", width=300),
        padding=ft.padding.all(8)
    )

    loader = ft.ProgressRing(width=50, height=50, visible=False, color=ft.Colors.PINK)

    # Prediction button click
    def predict_click(e):
        # Validate all fields
        fields = [
            age.content.value, sex.content.value, chest_pain.content.value, blood_pressure.content.value, cholesterol.content.value,
            fasting_bs.content.value, rest_ecg.content.value, max_hr.content.value, exercise_angina.content.value,
            oldpeak.content.value, slope.content.value, ca.content.value, thal.content.value
        ]

        if "" in fields or None in fields:
            result_value = "⚠️ Please fill all fields!"
            color = ft.Colors.ORANGE  # Ensure using Colors enum here
        else:
            loader.visible = True
            loader.update()

            try:
                # Prepare input
                input_data = np.array([[  
                    int(age.content.value),
                    1 if sex.content.value == "Male" else 0,
                    int(chest_pain.content.value),
                    int(blood_pressure.content.value),
                    int(cholesterol.content.value),
                    int(fasting_bs.content.value),
                    int(rest_ecg.content.value),
                    int(max_hr.content.value),
                    1 if exercise_angina.content.value == "Yes" else 0,
                    float(oldpeak.content.value),
                    int(slope.content.value),
                    int(ca.content.value),
                    int(thal.content.value)
                ]])

                prediction = model.predict(input_data)

                if prediction[0] == 1:
                    result_value = "❤️‍🔥 Warning: Heart Disease Detected!"
                    color = ft.Colors.RED  # Use Colors enum for color
                else:
                    result_value = "💚 No Heart Disease Detected."
                    color = ft.Colors.GREEN  # Use Colors enum for color

            except Exception as ex:
                result_value = f"Error: {str(ex)}"
                color = ft.Colors.RED  # Use Colors enum for color

            loader.visible = False
            loader.update()

            # Show result in a dialog box
            show_result_dialog(result_value, color)

    # Show the result in a dialog
    def show_result_dialog(result_value, color):
        result_dialog = ft.AlertDialog(
            title=ft.Text(  # Ensure title is a Text component
                value="Prediction Result",
                size=25,
                weight="bold",
                color=ft.Colors.PINK,  # Title color
                text_align="center"
            ),
            content=ft.Text(
                value=result_value,
                size=25,
                weight="bold",
                color=color,  # Content color
                text_align="center"
            ),
            actions=[ft.TextButton("Close", on_click=lambda e: setattr(result_dialog, "open", False))]
        )
        page.add(result_dialog)
        result_dialog.open = True
        page.update()

    # Wrap the button in a Container for padding and styling
    predict_button_container = ft.Container(
        content=ft.ElevatedButton(
            text="Predict",
            on_click=predict_click,
            color="white",
            bgcolor=ft.Colors.PINK,
            width=300,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=15))
        ),
        padding=ft.padding.all(12)
    )

    # Layout
    page.add(
        ft.Column(
            [
                title,
                loader,
                age, sex, chest_pain, blood_pressure, cholesterol,
                fasting_bs, rest_ecg, max_hr, exercise_angina, oldpeak,
                slope, ca, thal,
                predict_button_container,  # Added the button container
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=20,
            expand=True,
            scroll="auto"
        )
    )

# Run the app
ft.app(target=main)
