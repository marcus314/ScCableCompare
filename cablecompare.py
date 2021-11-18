import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk    #https://realpython.com/python-gui-tkinter/

#increase plt font size a bit
font = {'size'   : 12}
plt.rc('font', **font)

root =tk.Tk()
root.title('Cablecomparer v0.2')

### The summands of the superconductor losses
str_sc_totalloss = tk.StringVar(root, value = 0) #in kW
str_sc_cryoloss = tk.StringVar(root, value = 2) # in kW
str_sc_dielloss = tk.StringVar(root, value = 0.3) #in kW
str_sc_pumploss = tk.StringVar(root, value = 0) #in kW
str_sc_remagloss = tk.StringVar(root, value = 0) #in kW

### The summands of the normal cable losses
str_nc_totalloss = tk.StringVar(root, value = 0) #in kW
str_nc_ohmloss = tk.StringVar(root, value = 0) # in kW
str_nc_dielloss = tk.StringVar(root, value = 0.3) #in kW
str_nc_skinloss = tk.StringVar(root, value = 0) # losses because of the skin effect in kW
str_nc_otherloss = tk.StringVar(root, value = 0) #in percentage of the ohmloss

### Values for the overall parameters of the transmission
str_para_frequency =  tk.StringVar(root, value = 50) #the frequency in Hz
str_para_length = tk.StringVar(root, value = 10) #length of the cable in km
str_para_voltage = tk.StringVar(root, value = 10) #the voltage in kV
str_para_power = tk.StringVar(root, value = 40000) # the power that is transmitted in kW
str_para_utilization = tk.StringVar(root, value = 0.7) # average utilization of the cable, between 0 and 1

### Values that are needed but not directly entered by the user
str_val_current = tk.StringVar(root, value = 0) # The total current flowing through the cables

### Declaration of lesser used, "specialized" variables
#needed for sc_cryoloss
str_sc_cables = tk.StringVar(root, value = 1) # Number of cables
str_sc_thermal = tk.StringVar(root, value = 2) # thermal loss in W/m
str_sc_ln2efficiency = tk.StringVar(root, value = 0.06) # effieciency of the nitrogen liquefaction between 0 and 1
#needed for sc_dielloss
str_sc_capacitance = tk.StringVar(root, value = (158*(10**-12))) # capacitance in F/m
str_sc_tand = tk.StringVar(root, value = (0.0003)) # loss factor tan(delta)
#needed for sc_pumploss
str_sc_pumps = tk.StringVar(root, value = 5) # energy needed for the pumps for each cable in kW
#needed for sc_remagloss
str_sc_irated = tk.StringVar(root, value = 3.6) # rated current of the SC cable in kA
# set directly, else calculated by using polynomial approximation

#needed for nc_ohmloss
str_nc_cables = tk.StringVar(root, value = 1) # number of cables
str_nc_diameter = tk.StringVar(root, value = 56) # diameter of the conductor in mm
str_nc_specresist = tk.StringVar(root, value = 0.01786) # specific resistance of the material of the conductor, default is for copper
#needed for nc_dielloss
str_nc_capacitance = tk.StringVar(root, value = (230*(10**-12))) # capacitance in pF/m
str_nc_tand = tk.StringVar(root, value = (0.003)) # loss factor tan(delta)
#needed for nc_skinloss
str_nc_mur = tk.StringVar(root, value = 1.26 * 10**-6) # the relative magnetic permeability of the conductor. Default of copper
#needed for nc_otherloss
str_nc_otherlossfactor = tk.StringVar(root, value = 0) # just this variable, in percent

# Variables needed for plotting
str_plt_start =  tk.StringVar(root, value = 1)
str_plt_end = tk.StringVar(root, value = 50000)

### Setting the main input fields in the main window
#frequency
lbl_enterfreq = tk.Label(root, text = "Enter frequency in Hz. Set 0 for DC").pack()
e_getfreq = tk.Entry(root,textvariable = str_para_frequency,width=100).pack()

#length
lbl_enterlength = tk.Label(root, text = "Enter length in km").pack()
e_getlenth = tk.Entry(root,textvariable = str_para_length,width=100).pack()

#get voltage to compare
lbl_entervoltage = tk.Label(root, text = "Enter voltage in kV").pack()
e_getvoltage = tk.Entry(root,textvariable = str_para_voltage,width=100).pack()

#get power
lbl_enterpower = tk.Label(root, text = "Enter power in kW").pack()
e_getpower = tk.Entry(root,textvariable = str_para_power,width=100).pack()

#get average usage
lbl_enterutilization = tk.Label(root, text = "Enter average utilization of transmission (between 0 and 1)").pack()
e_getutilization = tk.Entry(root,textvariable = str_para_utilization,width=100).pack()


###Functions, to calculate the losses. They return their respective losses
#calculates the eneregy needed to supply the cryostat in W/m
def calc_sc_cryoloss():
    para_length = float(str_para_length.get())
    sc_cables = float(str_sc_cables.get())
    sc_thermal = float(str_sc_thermal.get())
    sc_ln2efficiency = float(str_sc_ln2efficiency.get())

    sc_cryoloss = (1/1000) * para_length * 1000 * sc_cables * sc_thermal * (1/sc_ln2efficiency)
    str_sc_cryoloss.set(sc_cryoloss)
    return sc_cryoloss

#calculates the dielectric losses of the superconductor in kW
def calc_sc_dielloss():
    para_length = float(str_para_length.get())
    sc_cables = float(str_sc_cables.get())
    para_frequency = float(str_para_frequency.get())
    sc_capacitance = float(str_sc_capacitance.get())
    para_voltage = 1000 * float(str_para_voltage.get())
    sc_tand = float(str_sc_tand.get())
    sc_ln2efficiency = float(str_sc_ln2efficiency.get())

    #print(f"{para_length},{sc_cables},{para_frequency},{sc_capacitance},{para_voltage},{sc_tand}") #DEBUG
    sc_dielloss = (1/1000) * para_length * 1000 * sc_cables * 2 * 3.14159 * para_frequency * sc_capacitance * np.power(para_voltage/np.sqrt(3),2) * sc_tand * (1/sc_ln2efficiency)
    str_sc_dielloss.set(sc_dielloss)
    return sc_dielloss

#calculates the energy needed to supply the pumps of the SC. Assumption: Pumps are needed every 10 km
def calc_sc_pumploss():
    sc_cables = float(str_sc_cables.get())
    sc_pumps = float(str_sc_pumps.get())
    para_length = float(str_para_length.get())

    sc_pumploss = sc_cables * sc_pumps * np.ceil(para_length/10)
    str_sc_pumploss.set(sc_pumploss)
    return sc_pumploss

#calculate the remagnisation losses of the SC in kW #TODO when using multiple cables utilization goes down accordingly
def calc_sc_remagloss():
    para_length = float(str_para_length.get())
    sc_cables = float(str_sc_cables.get())
    para_frequency = float(str_para_frequency.get())
    sc_irated = float(str_sc_irated.get())
    sc_ln2efficiency = float(str_sc_ln2efficiency.get())
    val_current = float(str_val_current.get())

    sc_currentdiv = (val_current/sc_cables)/(sc_irated*1000)
    print(f"I0/Ir = {sc_currentdiv} I0 = {val_current}") #DEBUG
    sc_remagloss = 0
    if sc_currentdiv > 0.36:
        sc_remagloss = (1/1000) * para_length * 1000 * sc_cables * (1/3200) * (para_frequency/50) * 0.5 * (22714.44* np.power(sc_currentdiv,3) - 10343.67 * np.power(sc_currentdiv,2) + 817.22 * sc_currentdiv) * (1/sc_ln2efficiency)
    str_sc_remagloss.set(sc_remagloss)
    return sc_remagloss

#calculate the total loss of the SC in kW
def calc_sc_totalloss():
    para_power = float(str_para_power.get())
    para_voltage = float(str_para_voltage.get())
    sc_irated = float(str_sc_irated.get()) *1000
    val_current = para_power/para_voltage
    str_val_current.set(val_current)

    if val_current > sc_irated:
        sc_cables = np.ceil((val_current/3)/(sc_irated)) * 3
        print(f"sc_cables: {sc_cables}")
    elif para_voltage > 110:
        sc_cables = 3
    else:
        sc_cables = 1
    
    str_sc_cables.set(sc_cables)
    #TODO Set nr of cables according to formula (3 cables for voltages over 110kV)
    sc_totalloss = calc_sc_cryoloss() + calc_sc_dielloss() + calc_sc_pumploss() + calc_sc_remagloss()
    str_sc_totalloss.set(sc_totalloss)


    #DEBUG IN THE FOLLOWING LINES
    sc_cryoloss = float(str_sc_cryoloss.get())
    sc_dielloss = float(str_sc_dielloss.get())
    sc_pumploss = float(str_sc_pumploss.get())
    sc_remagloss = float(str_sc_remagloss.get())
    print(f"SC: cryo: {sc_cryoloss} , diel: {sc_dielloss} , pump: {sc_pumploss} , remag: {sc_remagloss}, total: {sc_totalloss}")

    #print(sc_totalloss)
    return sc_totalloss

#calculates the ohmic losses in kW
def calc_nc_ohmloss():
    nc_cables = float(str_nc_cables.get())
    para_length = 1000 * float(str_para_length.get())
    nc_specresist = float(str_nc_specresist.get())
    nc_radius = 0.5 * float(str_nc_diameter.get())
    val_current = float(str_val_current.get())

    nc_ohmloss = (1/1000) * (para_length * (nc_specresist)/(nc_cables * 3.14159*nc_radius**2)) * (val_current**2)
    str_nc_ohmloss.set(nc_ohmloss)
    return nc_ohmloss

def calc_nc_dielloss():
    para_length = float(str_para_length.get()) * 1000
    nc_cables = float(str_nc_cables.get())
    para_frequency = float(str_para_frequency.get())
    nc_capacitance = float(str_nc_capacitance.get())
    para_voltage = 1000 * float(str_para_voltage.get())
    nc_tand = float(str_nc_tand.get())

    #print(f"{para_length},{sc_cables},{para_frequency},{sc_capacitance},{para_voltage},{sc_tand}") #DEBUG
    nc_dielloss = (1/1000) * para_length * nc_cables * 2 * 3.14159 * para_frequency * nc_capacitance * np.power(para_voltage/np.sqrt(3),2) * nc_tand
    str_nc_dielloss.set(nc_dielloss)
    return nc_dielloss

#calculates the losses because of the skin effet in kW
def calc_nc_skinloss():
    para_length = float(str_para_length.get()) * 1000
    nc_cables = float(str_nc_cables.get())
    nc_diameter = float(str_nc_diameter.get()) * 10 ** -3
    para_frequency = float(str_para_frequency.get())
    nc_mur = float(str_nc_mur.get())
    nc_resistivity = float(str_nc_specresist.get()) * 10**-6
    val_current = float(str_val_current.get())

    mu0 = 4 * 3.14159 * 10**-7

    if para_frequency > 0:
        nc_skindepth = np.sqrt((nc_resistivity)/(2 * 3.14159 * para_frequency * nc_mur * mu0)) # something here is wrong! should be 9,4 mm
        nc_skindepth = 9.4 * 10 ** -3 #DEBUG ONLY! HAS TO BE CHANGED
        print(f"skindepth: {nc_skindepth}")
        nc_skinloss = (1/1000) * ((val_current/nc_cables) ** 2) * (para_length * nc_resistivity)/(3.14159 * (nc_diameter - nc_skindepth) * nc_skindepth)
    else:
        nc_skinloss = 0
    str_nc_skinloss.set(nc_skinloss)
    return nc_skinloss

#approximates other losses because of proximity effect, corona discharges
def calc_nc_otherloss():
    nc_otherlossfactor = float(str_nc_otherlossfactor.get())
    nc_ohmloss = float(str_nc_ohmloss.get())

    nc_otherloss = nc_ohmloss * nc_otherlossfactor / 100
    str_nc_otherloss.set(nc_otherloss)
    return nc_otherloss

def calc_nc_totalloss():
    


    nc_totalloss = calc_nc_ohmloss() + calc_nc_dielloss() + calc_nc_skinloss() + calc_nc_otherloss()
    str_nc_totalloss.set(nc_totalloss)

    #DEBUG IN THE FOLLOWING LINES:
    nc_ohmloss = float(str_nc_ohmloss.get())
    nc_dielloss = float(str_nc_dielloss.get())
    nc_skinloss = float(str_nc_skinloss.get())
    nc_otherloss = float(str_nc_otherloss.get())
    print(f"NC: ohm: {nc_ohmloss}, diel: {nc_dielloss}, skin: {nc_skinloss}, other: {nc_otherloss}, total: {nc_totalloss}")
    return nc_totalloss

def calc_compare():
    calc_sc_totalloss()
    calc_nc_totalloss()

### COMMANDS FOR PLOTTING
def plot_power():
    
    plt_start = float(str_plt_start.get())
    plt_end = float(str_plt_end.get())
    para_voltage = float(str_para_voltage.get())
    para_length = float(str_para_length.get())
    para_frequency = float(str_para_frequency.get())
    
    xval = np.linspace(plt_start, plt_end, 100)
    yval_nc = np.zeros((len(xval)))
    yval_sc = np.zeros((len(xval)))
    for i in range(len(xval)):
        print(f"run {i}") #DEBUG
        str_para_power.set(xval[i])
        yval_sc[i] = calc_sc_totalloss()
        yval_nc[i] = calc_nc_totalloss()
    
    xval = xval/1000
    plt.plot(xval,yval_sc, label = "Superconductor", linewidth=3)
    plt.plot(xval,yval_nc, label = "Conventional cable", linewidth=3)
    plt.title(f"Length: {para_length} km, Voltage: {para_voltage} kV, freq: {para_frequency} Hz ")
    plt.xlabel("Power transmitted in MW")
    plt.ylabel("Power lost in kW")
    plt.legend()
    plt.grid()
    plt.show()
    return 0




### the other windows

# The window where cable specific variables can be set
def openVarWindow():
    varWindow = tk.Toplevel(root)
    # sets the title of the Toplevel widget
    varWindow.title("Var Window")
    # sets the geometry of toplevel
    varWindow.geometry("550x700")
    tk.Label(varWindow, text ="Options to adjust the cable specific variables").pack()

    #thermal losses of the superconductor in W/m
    tk.Label(varWindow, text = "-------------------------Variables fo the superconducting cable: -------------------------").pack()
    tk.Label(varWindow, text = "Thermal losses of the superconductor in W/m").pack()
    tk.Entry(varWindow,textvariable = str_sc_thermal,width=10).pack()

    tk.Label(varWindow, text = "Efficiency of the nitrogen liquefaction (between 0.0 and 1.0)").pack()
    tk.Entry(varWindow,textvariable = str_sc_ln2efficiency,width=10).pack()
    #
    tk.Label(varWindow, text = "Capacitance of the superconductor cable in F/m").pack() #TODO: Maybe change to pF/m and calculate accordingly?
    tk.Entry(varWindow,textvariable = str_sc_capacitance,width=10).pack()
    #
    tk.Label(varWindow, text = "Dielectric loss factor tan(delta) for the superconductor").pack()
    tk.Entry(varWindow,textvariable = str_sc_tand,width=10).pack()
    #
    tk.Label(varWindow, text = "Power needed for the pumps for each superconductor cable in kW").pack()
    tk.Entry(varWindow,textvariable = str_sc_pumps,width=10).pack()
    #
    tk.Label(varWindow, text = "Rated current for each superconducting cable in kA").pack()
    tk.Entry(varWindow,textvariable = str_sc_irated,width=10).pack()

    tk.Label(varWindow, text = "-------------------- Variables for the conventional cable: --------------------").pack()
    #
    tk.Label(varWindow, text = "Number of conventional cables cables").pack()
    tk.Entry(varWindow,textvariable = str_nc_cables,width=10).pack()
    #
    tk.Label(varWindow, text = "Diameter of each cable in mm").pack()
    tk.Entry(varWindow,textvariable = str_nc_diameter,width=10).pack()
    #
    tk.Label(varWindow, text = "Specific resistance of the conducting material in Ohm*mm^2/m").pack()
    tk.Entry(varWindow,textvariable = str_nc_specresist,width=10).pack()
    #
    tk.Label(varWindow, text = "Dielectric loss factor tan(delta) for the conventional cable").pack()
    tk.Entry(varWindow,textvariable = str_nc_capacitance,width=10).pack()
    #
    tk.Label(varWindow, text = "Dielectric loss factor tan(delta) for the conventional cable in F/m").pack()
    tk.Entry(varWindow,textvariable = str_nc_tand,width=10).pack()
    #
    tk.Label(varWindow, text = "Relative magnetic permeability of the conducting material").pack()
    tk.Entry(varWindow,textvariable = str_nc_mur,width=10).pack()
    #
    tk.Label(varWindow, text = "Lossfactor for other effects like proximity effect and corona discharges, in percent of ohmic losses").pack()
    tk.Entry(varWindow,textvariable = str_nc_otherlossfactor,width=10).pack()


# A window that contains options to vary variables and plot the changes
def openPlotWindow():

    plotWindow = tk.Toplevel(root)
    # sets the title of the Toplevel widget
    plotWindow.title("Plot Window")
    # sets the geometry of toplevel
    plotWindow.geometry("300x500")
    tk.Label(plotWindow, text ="Here the options for plots shall be displayed").pack()

    tk.Label(plotWindow, text = "Set start and end point for plot:").pack()
    tk.Entry(plotWindow,textvariable = str_plt_start,width=10).pack()
    tk.Entry(plotWindow,textvariable = str_plt_end,width=10).pack()

    tk.Button(plotWindow, text = "Plot Power", command=plot_power).pack() 
    #tk.Button(plotWindow, text = "Plot Utilizatiogn", command=plotUtilization).pack()
    #tk.Button(plotWindow, text = "Plot Loadfactor", command=plotLoadfactor).pack() 




btn_calcploss = tk.Button(root, text = "Calc ploss", command=calc_compare).pack()    
#display resut of ploss
lbl_showploss = tk.Label(root, text = "Total loss of the conventional cable in kW").pack()
lbl_ploss = tk.Label(root, textvariable = str_nc_totalloss).pack()
lbl_showploss = tk.Label(root, text = "Total loss of the superconductor cable in kW").pack()
#thisstring = tk.StringVar(root, value = str_calcscloss)
lbl_ploss = tk.Label(root, textvariable = str_sc_totalloss).pack() #str_calcscloss
#but2 = tk.Button(root, text = "Plot Utilizatiogn", command=plotUtilization()).pack() 
tk.Button(root, text = "Open Plots", command=openPlotWindow).pack()
tk.Button(root, text = "Open Variables", command=openVarWindow).pack()


'''

# calculate the P_loss
def calcploss():
    #plt.plot(array_a)
    #Get all the values in base units
    length, power, voltage, utilization, frequency, sc_lN2_efficiency, sc_heatloss, sc_dielloss, sc_ACloss, loadfactor, sc_nrofcables, nc_specresist = getall()
    #length = float(str_getlength.get()) * 1000
    #power = float(str_getpower.get())*1000
    #voltage = float(str_getvoltage.get()) * 1000
    #utilization = float(str_getutilization.get())
    #frequency = float(str_getfreq.get())
    #sc_lN2_efficiency = float(str_sc_lN2_efficiency.get())
    #sc_heatloss = float(str_sc_heatloss.get())
    #sc_dielloss = float(str_sc_dielloss.get())
    #sc_ACloss = float(str_sc_ACloss.get())
    #loadfactor = float(str_loadfactor.get())
    #sc_nrofcables = float(str_sc_nrofcables.get())

    pncloss = calcncloss(length, nc_specresist, power, voltage, utilization, frequency)
    str_calcpncloss.set(pncloss)
    cc_losspercentage = (pncloss/power) * 100
    

    pscloss = calcscloss(length, nc_specresist, power, voltage, utilization, frequency, loadfactor, sc_lN2_efficiency,sc_heatloss,sc_dielloss,sc_ACloss, sc_nrofcables)
    
    sc_losspercentage = (pscloss / power) * 100
    str_calcscloss.set(pscloss)
    print(f"P_loss = {pncloss} W which is {cc_losspercentage}% of power transmitted\nSuperconductor looses {pscloss} W which is {sc_losspercentage}%")
    #plt.show()

def calcncloss(length, nc_specresist, power, voltage, utilization, frequency):
    current = power/voltage
    pncloss = 0
    pncloss += length * current * current * nc_specresist * utilization 
    #The following claculates the loss for AC transmission. TODO: A more sophisticated formula is needed here
    if frequency != 0:
        pncloss *= 1.05
    pncloss = int(pncloss)
    return pncloss

def calcscloss(length, specresist, power, voltage, utilization, frequency, loadfactor, sc_lN2_efficiency,sc_heatloss,sc_dielloss,sc_ACloss, sc_nrofcables):
    pscloss= sc_heatloss * length * (1/sc_lN2_efficiency)
    if(frequency) != 0:
        pscloss += sc_dielloss * length * (1/sc_lN2_efficiency)
        if(loadfactor > 0.36):
            ACloss = (1/3200) * (frequency/50) * 0.5 * (22714.44* np.power(loadfactor,3) - 10343.67 * np.power(loadfactor,2) + 817.22 * loadfactor ) * length
            print(f"run with loadfactor {loadfactor}") #DEBUG
            #print(f"ACloss = {ACloss/length} per meter")
            pscloss += ACloss
    pscloss = int(pscloss * sc_nrofcables)
    print(f"Current is {power/voltage} A")
    return pscloss

#returns all the variables
def getall():
    length = float(str_getlength.get()) * 1000
    power = float(str_getpower.get())*1000
    voltage = float(str_getvoltage.get()) * 1000
    utilization = float(str_getutilization.get())
    frequency = float(str_getfreq.get())
    sc_lN2_efficiency = float(str_sc_lN2_efficiency.get())
    sc_heatloss = float(str_sc_heatloss.get())
    sc_dielloss = float(str_sc_dielloss.get())
    sc_ACloss = float(str_sc_ACloss.get())
    loadfactor = float(str_loadfactor.get())
    sc_nrofcables = float(str_sc_nrofcables.get())
    nc_specresist = float(str_nc_specresist.get())
    return length, power, voltage, utilization, frequency, sc_lN2_efficiency, sc_heatloss, sc_dielloss, sc_ACloss, loadfactor, sc_nrofcables, nc_specresist

#Plot functions for the plot window
def plotUtilization():
    length, power, voltage, utilization, frequency, sc_lN2_efficiency, sc_heatloss, sc_dielloss, sc_ACloss, loadfactor, sc_nrofcables, nc_specresist = getall()
    xval = np.linspace(0,1,20)
    sc_vals = np.zeros((20))
    nc_vals = np.zeros((20))
    for i in range(20):
        sc_vals[i] = calcscloss(length, nc_specresist, power, voltage, xval[i], frequency, loadfactor, sc_lN2_efficiency,sc_heatloss,sc_dielloss,sc_ACloss, sc_nrofcables)/1000
        nc_vals[i] = calcncloss(length, nc_specresist, power, voltage, xval[i], frequency)/1000
    plt.plot(xval,sc_vals, label = "superconductor")
    plt.plot(xval,nc_vals, label = "conventional cable")
    plt.xlabel("Utilization")
    plt.ylabel("Total power loss in kW")
    plt.legend()
    plt.show()

def plotLoadfactor():
    length, power, voltage, utilization, frequency, sc_lN2_efficiency, sc_heatloss, sc_dielloss, sc_ACloss, loadfactor, sc_nrofcables, nc_specresist = getall()
    xval = np.linspace(0,1,20)
    sc_vals = np.zeros((20))
    nc_vals = np.zeros((20))
    for i in range(20):
        sc_vals[i] = calcscloss(length, nc_specresist, power, voltage, utilization, frequency, xval[i], sc_lN2_efficiency,sc_heatloss,sc_dielloss,sc_ACloss, sc_nrofcables)/1000
        nc_vals[i] = calcncloss(length, nc_specresist, power, voltage, utilization, frequency)/1000
    plt.plot(xval,sc_vals, label = "superconductor")
    plt.plot(xval,nc_vals, label = "conventional cable")
    plt.xlabel("Loadfactor")
    plt.ylabel("Total power loss in kW")
    plt.legend()
    plt.show()    



# A window that offers the possibility to change Variables, that are not needed to be changed that often
def openVarWindow():
    varWindow = tk.Toplevel(root)
    # sets the title of the Toplevel widget
    varWindow.title("Var Window")
    # sets the geometry of toplevel
    varWindow.geometry("500x500")
    tk.Label(varWindow, text ="Here the options to adjust rarely used variables").pack()

    #Set the efficiency of the lN2 liquification and cooling to 77K
    tk.Label(varWindow, text = "Efficiency of the lN2 liquification+cooling (between 0.0 and 1.0").pack()
    tk.Entry(varWindow,textvariable = str_sc_lN2_efficiency,width=10).pack()
    
    tk.Label(varWindow, text = "Cryostat loss in W/m").pack()
    tk.Entry(varWindow,textvariable = str_sc_heatloss,width=10).pack()
    
    tk.Label(varWindow, text = "Superconductor dielectric loss in W/m").pack()
    tk.Entry(varWindow,textvariable = str_sc_dielloss,width=10).pack()

    tk.Label(varWindow, text = "Superconductor AC loss in W/m").pack()
    tk.Entry(varWindow,textvariable = str_sc_ACloss,width=10).pack()

    tk.Label(varWindow, text = "Superconductor loadfactor (must be between 0.0 and 1.0").pack()
    tk.Entry(varWindow,textvariable = str_loadfactor,width=10).pack()

    tk.Label(varWindow, text = "Resistance of the normal cable in Ohm/m").pack()
    tk.Entry(varWindow,textvariable = str_nc_specresist,width=10).pack()


# A window that contains options to vary variables and plot the changes
def openPlotWindow():
    #Get all the values in base units
    length, power, voltage, utilization, frequency, sc_lN2_efficiency, sc_heatloss, sc_dielloss, sc_ACloss, loadfactor, sc_nrofcables, nc_specresist = getall()

    plotWindow = tk.Toplevel(root)
    # sets the title of the Toplevel widget
    plotWindow.title("Plot Window")
    # sets the geometry of toplevel
    plotWindow.geometry("300x500")
    tk.Label(plotWindow, text ="Here the options for plots shall be displayed").pack()
    tk.Button(plotWindow, text = "Plot Utilizatiogn", command=plotUtilization).pack()
    tk.Button(plotWindow, text = "Plot Loadfactor", command=plotLoadfactor).pack() 





btn_calcploss = tk.Button(root, text = "Calc ploss", command=calcploss).pack()    
#display resut of ploss
lbl_showploss = tk.Label(root, text = "Total loss of the conventional cable").pack()
lbl_ploss = tk.Label(root, textvariable = str_calcpncloss).pack()
lbl_showploss = tk.Label(root, text = "Total loss of the superconductor cable").pack()
thisstring = tk.StringVar(root, value = str_calcscloss)
lbl_ploss = tk.Label(root, textvariable = str_calcscloss ).pack() #str_calcscloss
#but2 = tk.Button(root, text = "Plot Utilizatiogn", command=plotUtilization()).pack() 

tk.Button(root, text = "Open Plots", command=openPlotWindow).pack()
tk.Button(root, text = "Open Variables", command=openVarWindow).pack()




'''

root.mainloop()


#SPACE FOR IDEAS
'''
Depending on the transmitted power, different cables should be used. The biggest I found were the best paths project cables from nexans that can transmit 10kA at 320 kV.
But here, 3 cables per phase are needed, so the losses per cable have to be taken times 3
110 kV with up to xA (maybe 3A) can be built in one cable


'''
