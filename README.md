# Sampling-Studio-Task

## Overview
Sampling Studio is a desktop application that showcases the principles of signal sampling and recovery, emphasizing the importance and validation of the Nyquist rate. Sampling an analog signal is a crucial step in digital signal processing systems, and the Nyquist-Shannon sampling theorem guarantees the accurate recovery of the original signal when sampled with a frequency greater than or equal to its bandwidth (or double the maximum frequency for real signals).


## Features
- **Sample & Recover**
  - This feature allows users to select an analog signal and sample it at a specified sampling rate. The sampled signal can then be recovered using various interpolation techniques, demonstrating the importance of the Nyquist rate.

- **Load and Compose**
  -  Users can load pre-recorded signals or compose their own signals using the provided signal generation tools. This feature enables the study of different signal characteristics and their impact on the sampling process.

- **Additive White Gaussian Noise**
  -  To simulate real-world scenarios, the application includes the option to introduce additive white Gaussian noise to the sampled signal. This feature helps users observe the effects of noise on the recovery process and understand the limitations of sampling in noisy environments.

- **Real-time Sampling and Recovery**
  -The application supports real-time sampling and recovery, allowing users to visualize the effects of changing sampling rates dynamically. This feature enhances the understanding of the Nyquist rate in real-time signal processing scenarios.

- **Responsive Desktop App**
  - The Sampling Theory Studio is designed as a responsive desktop application, providing an intuitive and user-friendly interface for an enhanced user experience.

## Demo


https://github.com/salsabilmostafa/Sampling_Studio-Task/assets/115428975/aed383c9-4d4d-4ef2-ac05-7f59e5c18aa5


## Usage
1. Clone the repository.
    ```bash
    git clone https://github.com/salsabilmostafa/Sampling_Studeio-Task.git
    ```
2. Run the application.
    ```bash
    python main.py
    ```
3. Use the "Sample & Recover" feature to select an analog signal and specify the sampling rate. Observe the recovered signal and compare it with the original signal.

4. Explore the "Load and Compose" feature to load pre-recorded signals or generate custom signals. Experiment with different signal characteristics and observe their effects on the sampling and recovery process.

5. Utilize the "Additive White Gaussian Noise" option to introduce noise to the sampled signal. Observe the impact of noise on the recovery quality and understand the limitations of sampling in noisy environments.

6. Explore the real-time sampling and recovery capabilities to visualize the effects of changing sampling rates dynamically. Observe the behavior of the recovered signal in real-time scenarios.


## Dependencies
Ensure you have the following dependencies installed before running the application:
- Python 3.7 or above
- PyQt5: Used for developing the responsive desktop application interface
- pandas: Provides data manipulation and analysis capabilities for efficient signal processing.
- numpy: Essential library for numerical computations and array operations.
- csv: Enables reading and writing of CSV files for data storage and analysis.

## Contributions
Contributions are welcome! If you find any bugs or have suggestions for improvements, feel free to open an issue or submit a pull request.
