# Trip-Reservation-System

IT 4320 final project

# Trip Reservation System

This project implements a web-based trip reservation system using Flask, a popular web framework in Python. The system allows users to reserve seats, and administrators can log in to view and manage reservations.

## Features

- **Seat Reservation**: Users can reserve available seats.
- **Admin Dashboard**: Administrators can log in to view the seating chart and total sales.
- **Dynamic Seating Chart**: Visual representation of available and reserved seats.
- **Responsive Design**: Web pages adapt to different screen sizes for better user experience.

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/your-repository-name.git
   ```

2. **Install Dependencies**

   Make sure you have Python installed. Then, install Flask:

   ```bash
   pip install Flask
   ```

3. **Run the Application**

   Navigate to the project directory and run:

   ```bash
   python app.py
   ```

   This will start the Flask server.

## Usage

- Access the home page at `http://127.0.0.1:5002/`.
- Choose to reserve a seat or log in as an administrator.
- Follow the on-screen instructions to make a reservation or view the admin dashboard.

## File Structure

- `app.py`: Main Flask application file.
- `reservation_utils.py`: Contains utility functions for handling reservations.
- `authentication_utils.py`: Functions for handling admin authentication.
- `admin_utils.py`: Functions specific to admin features like calculating total sales.
- `templates/`: Folder containing HTML templates for different pages.
- `data_files/`: Folder containing data files like reservations and admin credentials.

## Contributing

Contributions to this project are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Commit your changes.
4. Push to the branch.
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any queries or contributions, please contact me at [your-email@example.com](mailto:your-email@example.com).
