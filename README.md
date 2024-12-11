# AgainToi
AgainToi is a Django-based platform for managing weddings and celebrity events. It features venue management, user and company profiles, and event scheduling, offering tailored solutions for seamless planning.

## Features

- **Venue Management:** Add, edit, and view detailed venue information.
- **User and Company Profiles:** Separate views and functionalities for individual users and companies.
- **Event Scheduling:** Plan, manage, and track events effortlessly.
- **Modular Architecture:** Designed with Django apps for scalability and maintainability.


## Installation

1. Clone the repository:
   ```bash
   git clone <https://github.com/daniyardautbaev/AgainToi.git>
   ```
2. Navigate to the project directory:
   ```bash
   cd AgainToi
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```
7. Open your browser and visit `http://127.0.0.1:8000` to access the application.

## How to Use

- **For Users:** Create an account, browse available venues, and plan your events.
- **For Companies:** Register as a company to manage venues and track bookings.

## Future Enhancements

- Payment gateway integration for seamless booking.
- Social media integration for event promotions.
- Advanced analytics and reporting features.

## Contributing

Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions and bug reports.

## License

This project is licensed under the [MIT License](LICENSE).
