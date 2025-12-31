# NutriPlan – Smart Nutrition Planner for Families

## Problem Statement
Families often fail to meet daily nutritional requirements due to unplanned meals and limited awareness of the nutritional value of commonly prepared home-cooked dishes. This leads to nutritional imbalance over time, even when meals are prepared regularly at home.

## Proposed Solution
NutriPlan is a simple and practical nutrition planning application designed to help families organize daily meals in a nutritionally balanced manner. The application allows users, especially homemakers, to select dishes they already know how to prepare. Each selected dish is associated with basic nutritional information.

Based on the selected dishes, the system generates a daily or weekly meal plan that distributes food items in a balanced way. To involve the entire family in the process, the application sends a reminder message to another family member through WhatsApp, informing them about the ingredients required for the next day’s meals. This shared approach improves nutrition awareness and meal planning consistency within the household.

## Features
- Selection of familiar home-cooked dishes
- Display of nutritional values for selected dishes
- Automatic daily and weekly meal planning
- Balanced meal distribution across the day
- WhatsApp-based reminder for ingredient planning
- Simple and user-friendly interface

## Data Flow Diagram (DFD)

### DFD Level 0
The user provides dish selection input to the system. The system processes the input using stored nutritional data and generates outputs in the form of a meal plan and ingredient notification.

### DFD Level 1
In the detailed data flow, the user interacts with the dish selection module. The selected dish data is passed to the nutrition processing module, which calculates the nutritional distribution. The meal planning module then creates a daily or weekly plan and forwards the ingredient list to the notification module. The final output is delivered to both the user and a family member through the application and WhatsApp message.

![DFD](https://github.com/user-attachments/assets/b045effc-10ae-4f54-b3b9-d122bb107827)



## Technology Stack
- HTML
- CSS
- Python
- Flask

## Prototype Description
This project includes a frontend prototype that demonstrates the core idea and workflow of the application. The nutritional values and WhatsApp notification are shown in a simulated manner for demonstration purposes. The prototype focuses on explaining the concept, user flow, and practical implementation of the solution.

## Future Scope
The application can be enhanced by integrating real-time nutrition databases, personalized diet recommendations based on age and health conditions, WhatsApp Business API for automated messaging, and additional features such as grocery list optimization and dietitian consultation support.

## Conclusion
NutriPlan aims to promote better nutrition planning for families by combining familiar cooking habits with structured meal planning. By increasing nutrition awareness and encouraging shared responsibility within the household, the application supports healthier and more balanced daily diets.


## For Login Purpose Use These Credentials:

USER_EMAIL = "himanshubora100@gmail.com"<br>
USER_PASSWORD = "12345678"


## Deployment Link:
https://nutriplan-c7ev.onrender.com






