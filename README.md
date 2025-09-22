# ECG Analysis with Secure ASCON-128

This project provides tools to analyze **electrocardiograms (ECG)** while ensuring secure communication over **UART** using **ASCON-128** encryption and decryption.

## Project Contents
 
- **PROJET_FPGA_ASCON_SV**: Source files and Vivado project used to generate the FPGA bitstream.  
- **Python Environment**: Scripts for ECG analysis:  
  - `ecg_plotter.py`: Uses **NeuroKit2** to detect **R peaks** with high precision.  
  - `ecg_plotter_err.py`: Uses `scipy.signal` to detect **PQRST peaks** with lower precision.  
  *To switch the analysis method, simply rename the script called in the project.*  
- **Presentation (PowerPoint)**: Detailed diagrams of the hardware architecture.

## Purpose

The project provides a complete environment for:  
- Secure processing of ECG signals on FPGA.  
- ECG signal analysis in Python.  
- Visualization and understanding of the hardware architecture.

## Notes

- The FPGA part requires **Vivado**.  
- Python scripts require **NeuroKit2** and **scipy**.  
- UART communication is secured via **ASCON-128** encryption.
