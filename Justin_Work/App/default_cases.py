import os
from PyQt5.QtWidgets import QMessageBox

def get_default_options(self):
    # Set default options based on the selected default
    print("Working")
    default_option = self.default_dropdown.currentText()

    with open(os.path.join(os.getcwd(), "Justin_Work", "App", "default_runs", default_option + ".txt"), 'r') as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())
            key, value = line.strip().split('~')
            key = key.strip()
            value = value.strip()
            if key == "Bellhop Executable":
                value = os.path.normpath(value)
                self.fields["Bellhop Executable"].setText(os.path.join(os.getcwd(), value))
            elif key == "SSP File":
                value = os.path.normpath(value)
                self.fields["SSP File"].setText(os.path.join(os.getcwd(), value))
            elif key == "Bathymetry File":
                value = os.path.normpath(value)
                self.fields["Bathymetry File"].setText(os.path.join(os.getcwd(), value))
            elif key == "Altimetry File":   
                value = os.path.normpath(value)
                self.fields["Altimetry File"].setText(os.path.join(os.getcwd(), value))
            elif key == "Data File Directory":
                value = os.path.normpath(value)
                self.fields["Data File Directory"].setText(os.path.join(os.getcwd(), value))
            elif key == "Filename":
                self.fields["Filename"].setText(value)
            elif key == "Source Longitude":
                self.fields["Source Longitude"].setText(value)  
            elif key == "Source Latitude":
                self.fields["Source Latitude"].setText(value)
            elif key == "Receiver Longitude":
                self.fields["Receiver Longitude"].setText(value)
            elif key == "Receiver Latitude":
                self.fields["Receiver Latitude"].setText(value)
            elif key == "Frequency":
                self.fields["Frequency"].setText(value)
            elif key == "SSPOPT(1)":
                self.fields["SSPOPT(1)"].setCurrentText(value)
            elif key == "SSPOPT(2)":
                self.fields["SSPOPT(2)"].setCurrentText(value)
            elif key == "SSPOPT(3)":
                self.fields["SSPOPT(3)"].setCurrentText(value)
            elif key == "SSPOPT(4)":    
                self.fields["SSPOPT(4)"].setCurrentText(value)
            elif key == "SSPOPT(5)":
                self.fields["SSPOPT(5)"].setCurrentText(value)
            elif key == "Surface Height":
                self.fields["Surface Height"].setText(value)
            elif key == "Surface Compressional Speed":
                self.fields["Surface Compressional Speed"].setText(value)
            elif key == "Surface Shear Speed":
                self.fields["Surface Shear Speed"].setText(value)
            elif key == "Surface Density":
                self.fields["Surface Density"].setText(value)
            elif key == "Surface Attenuation":  
                self.fields["Surface Attenuation"].setText(value)
            elif key == "Bottom Type":
                self.fields["Bottom Type"].setCurrentText(value)
            elif key == "Include Bathymetry":   
                self.fields["Include Bathymetry"].setCurrentText(value)
            elif key == "Roughness":
                self.fields["Roughness"].setText(value)
            elif key == "Bottom Height":
                self.fields["Bottom Height"].setText(value)
            elif key == "Bottom Compressional Speed":
                self.fields["Bottom Compressional Speed"].setText(value)
            elif key == "Bottom Shear Speed":
                self.fields["Bottom Shear Speed"].setText(value)
            elif key == "Bottom Density":
                self.fields["Bottom Density"].setText(value)
            elif key == "Bottom Attenuation":
                self.fields["Bottom Attenuation"].setText(value)
            elif key == "Number of Source Depths":
                self.fields["Number of Source Depths"].setText(value)
            elif key == "Source Depths":
                self.fields["Source Depths"].setText(value)
            elif key == "Number of Receiver Depths":
                self.fields["Number of Receiver Depths"].setText(value)
            elif key == "Receiver Depths":
                self.fields["Receiver Depths"].setText(value)
            elif key == "Number of Receiver Ranges":
                self.fields["Number of Receiver Ranges"].setText(value)
            elif key == "Receiver Ranges":
                self.fields["Receiver Ranges"].setText(value)
            elif key == "Ray Compute Type":
                self.fields["Ray Compute Type"].setCurrentText(value)
            elif key == "Number of Beams":
                self.fields["Number of Beams"].setText(value)
            elif key == "Launch Angles":
                self.fields["Launch Angles"].setText(value)
            elif key == "Step Size":
                self.fields["Step Size"].setText(value)
            else:
                QMessageBox.warning(self, "Warning", f"Field '{key}' not found in the form.")


def set_default_options(self):
    # Set default options based on the selected default
    default_option = self.default_dropdown.currentText()

    if default_option == "Eigenrays":
        self.fields["Bellhop Executable"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bellhop_exe", "bellhopcxx"))
        self.fields["SSP File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "ssp.mat"))
        self.fields["Bathymetry File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "bty.mat"))
        self.fields["Altimetry File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "ati.mat"))
        self.fields["Data File Directory"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "Runs"))
        self.fields["Filename"].setText("run_eigenrays_3500")
        self.fields["Source Longitude"].setText("-122.83")
        self.fields["Source Latitude"].setText("47.77")
        self.fields["Receiver Longitude"].setText("-122.85")
        self.fields["Receiver Latitude"].setText("47.71")
        self.fields["Frequency"].setText("3500.0")
        self.fields["SSPOPT(1)"].setCurrentText("S: Cubic Spline Interpolation")
        self.fields["SSPOPT(2)"].setCurrentText("A: Acoustic half-space (Surface information required)")
        self.fields["SSPOPT(3)"].setCurrentText("F: attenuation corresponds to (dB/m)kHz")
        self.fields["SSPOPT(4)"].setCurrentText("' ': Default parameter")   
        self.fields["SSPOPT(5)"].setCurrentText("*: Use if including an *.ati file for surface shape")
        self.fields["Surface Height"].setText("0.0")
        self.fields["Surface Compressional Speed"].setText("343.0")
        self.fields["Surface Shear Speed"].setText("0.0")
        self.fields["Surface Density"].setText("1.2")
        self.fields["Surface Attenuation"].setText("0.0")
        self.fields["Bottom Type"].setCurrentText("A: acoustic half-space below water column (need BOTTOM-LINE)")
        self.fields["Include Bathymetry"].setCurrentText("*: include if wanting to use a *.bty file")
        self.fields["Roughness"].setText("0.0")
        self.fields["Bottom Height"].setText("0.0")
        self.fields["Bottom Compressional Speed"].setText("1600.0")
        self.fields["Bottom Shear Speed"].setText("0.0")
        self.fields["Bottom Density"].setText("1.8")
        self.fields["Bottom Attenuation"].setText("0.0")
        self.fields["Number of Source Depths"].setText("1")
        self.fields["Source Depths"].setText("20.0")
        self.fields["Number of Receiver Depths"].setText("1")
        self.fields["Receiver Depths"].setText("20.0")
        self.fields["Number of Receiver Ranges"].setText("1")
        self.fields["Receiver Ranges"].setText("7.0")
        self.fields["Ray Compute Type"].setCurrentText("E: Write Eigenray coordinates")
        self.fields["Number of Beams"].setText("10001")
        self.fields["Launch Angles"].setText("-25.0, 25.0")
        self.fields["Step Size"].setText("10.0")

    elif default_option == "Ray Coordinates":
        self.fields["Bellhop Executable"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bellhop_exe", "bellhopcxx"))
        self.fields["SSP File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "ssp.mat"))
        self.fields["Bathymetry File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "bty.mat"))
        self.fields["Altimetry File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "ati.mat"))
        self.fields["Data File Directory"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "Runs"))
        self.fields["Filename"].setText("run_ray_coor_3500")
        self.fields["Source Longitude"].setText("-122.83")
        self.fields["Source Latitude"].setText("47.77")
        self.fields["Receiver Longitude"].setText("-122.85")
        self.fields["Receiver Latitude"].setText("47.71")
        self.fields["Frequency"].setText("3500.0")
        self.fields["SSPOPT(1)"].setCurrentText("S: Cubic Spline Interpolation")
        self.fields["SSPOPT(2)"].setCurrentText("A: Acoustic half-space (Surface information required)")
        self.fields["SSPOPT(3)"].setCurrentText("F: attenuation corresponds to (dB/m)kHz")
        self.fields["SSPOPT(4)"].setCurrentText("' ': Default parameter")   
        self.fields["SSPOPT(5)"].setCurrentText("*: Use if including an *.ati file for surface shape")
        self.fields["Surface Height"].setText("0.0")
        self.fields["Surface Compressional Speed"].setText("343.0")
        self.fields["Surface Shear Speed"].setText("0.0")
        self.fields["Surface Density"].setText("1.2")
        self.fields["Surface Attenuation"].setText("0.0")
        self.fields["Bottom Type"].setCurrentText("A: acoustic half-space below water column (need BOTTOM-LINE)")
        self.fields["Include Bathymetry"].setCurrentText("*: include if wanting to use a *.bty file")
        self.fields["Roughness"].setText("0.0")
        self.fields["Bottom Height"].setText("0.0")
        self.fields["Bottom Compressional Speed"].setText("1600.0")
        self.fields["Bottom Shear Speed"].setText("0.0")
        self.fields["Bottom Density"].setText("1.8")
        self.fields["Bottom Attenuation"].setText("0.0")
        self.fields["Number of Source Depths"].setText("1")
        self.fields["Source Depths"].setText("20.0")
        self.fields["Number of Receiver Depths"].setText("1")
        self.fields["Receiver Depths"].setText("20.0")
        self.fields["Number of Receiver Ranges"].setText("1")
        self.fields["Receiver Ranges"].setText("7.0")
        self.fields["Ray Compute Type"].setCurrentText("R: Write ray coordinates")
        self.fields["Number of Beams"].setText("10001")
        self.fields["Launch Angles"].setText("-89.0, 89.0")
        self.fields["Step Size"].setText("10.0")
        
    elif default_option == "Coherent Transmission Loss":
        self.fields["Bellhop Executable"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bellhop_exe", "bellhopcxx"))
        self.fields["SSP File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "ssp.mat"))
        self.fields["Bathymetry File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "bty.mat"))
        self.fields["Altimetry File"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "bty_ssp_ati", "ati.mat"))
        self.fields["Data File Directory"].setText(os.path.join(os.getcwd(), "Justin_Work", "App", "Runs"))
        self.fields["Filename"].setText("run_tl_3500")
        self.fields["Source Longitude"].setText("-122.83")
        self.fields["Source Latitude"].setText("47.77")
        self.fields["Receiver Longitude"].setText("-122.85")
        self.fields["Receiver Latitude"].setText("47.71") 
        self.fields["Frequency"].setText("3500.0")
        self.fields["SSPOPT(1)"].setCurrentText("S: Cubic Spline Interpolation")
        self.fields["SSPOPT(2)"].setCurrentText("V: Vacuum above surface (SURFACE-LINE not required)")
        self.fields["SSPOPT(3)"].setCurrentText("F: attenuation corresponds to (dB/m)kHz")
        self.fields["SSPOPT(4)"].setCurrentText("' ': Default parameter")   
        self.fields["SSPOPT(5)"].setCurrentText("*: Use if including an *.ati file for surface shape")
        self.fields["Surface Height"].setText("0.0")
        self.fields["Surface Compressional Speed"].setText("343.0")
        self.fields["Surface Shear Speed"].setText("0.0")
        self.fields["Surface Density"].setText("1.2")
        self.fields["Surface Attenuation"].setText("0.0")
        self.fields["Bottom Type"].setCurrentText("A: acoustic half-space below water column (need BOTTOM-LINE)")
        self.fields["Include Bathymetry"].setCurrentText("*: include if wanting to use a *.bty file")
        self.fields["Roughness"].setText("0.0")
        self.fields["Bottom Height"].setText("0.0")
        self.fields["Bottom Compressional Speed"].setText("1600.0")
        self.fields["Bottom Shear Speed"].setText("0.0")
        self.fields["Bottom Density"].setText("1.8")
        self.fields["Bottom Attenuation"].setText("0.0")
        self.fields["Number of Source Depths"].setText("1")
        self.fields["Source Depths"].setText("20.0")
        self.fields["Number of Receiver Depths"].setText("201")
        self.fields["Receiver Depths"].setText("0.0, 200.0")
        self.fields["Number of Receiver Ranges"].setText("501")
        self.fields["Receiver Ranges"].setText("0.0, 7.0")
        self.fields["Ray Compute Type"].setCurrentText("C: Write coherent acoustic pressure")
        self.fields["Number of Beams"].setText("0")
        self.fields["Launch Angles"].setText("-89.0, 89.0")
        self.fields["Step Size"].setText("0.0")