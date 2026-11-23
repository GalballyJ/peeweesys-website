# Import verified Porsche 986 Boxster S ME7.2 (y966ohc.ori) functions, calibration maps/axes, and RAM variables.
#@author ME72-Boxster-ECU-Project
#@category Porsche.ME72
#@keybinding
#@menupath
#@toolbar

from ghidra.program.model.symbol import SourceType

# Total symbols: 303
#   Campaign functions : 31
#   Campaign tables    : 3
#   VERIFIED_TUNER maps: 72
#   VERIFIED_TUNER axes: 97
#   Confirmed RAM vars : 86
#   RAM mirror addrs   : 14
SYMBOLS = [
  [
    "KWP_Dispatch_0x10_PID",
    8538620,
    "f",
    "KWP2000 SID 0x10 StartDiagnosticSession / PID dispatcher"
  ],
  [
    "KWP_0x11_ECUReset",
    8539068,
    "f",
    "KWP2000 SID 0x11 ECUReset handler"
  ],
  [
    "KWP_0x1A_ReadECUId",
    8539274,
    "f",
    "KWP2000 SID 0x1A ReadECUIdentification handler"
  ],
  [
    "KWP_0x21_ReadLID",
    8528170,
    "f",
    "KWP2000 SID 0x21 ReadDataByLocalIdentifier handler"
  ],
  [
    "KWP_0x22_ReadDataByCommonId",
    8529850,
    "f",
    "KWP2000 SID 0x22 ReadDataByCommonIdentifier handler"
  ],
  [
    "KWP_0x23_ReadMem",
    8529926,
    "f",
    "KWP2000 SID 0x23 ReadMemoryByAddress handler"
  ],
  [
    "KWP_0x27_SecurityAccess",
    8538886,
    "f",
    "KWP2000 SID 0x27 SecurityAccess handler"
  ],
  [
    "KWP_0x27_LFSR_Core",
    8540158,
    "f",
    "KWP2000 SID 0x27 seed/key LFSR core routine"
  ],
  [
    "KWP_0x2C_DDLI",
    8528522,
    "f",
    "KWP2000 SID 0x2C DynamicallyDefineLocalIdentifier handler"
  ],
  [
    "KWP_0x2C_Validator1",
    8535466,
    "f",
    "KWP2000 SID 0x2C DDLI address/range validator 1"
  ],
  [
    "KWP_0x2C_Validator2",
    8535832,
    "f",
    "KWP2000 SID 0x2C DDLI address/range validator 2"
  ],
  [
    "KWP_0x21_DynamicLID",
    8533308,
    "f",
    "KWP2000 SID 0x21 dynamic LID (0xF0+) reader"
  ],
  [
    "KWP_0x31_StartRoutine",
    8543274,
    "f",
    "KWP2000 SID 0x31 StartRoutineByLocalIdentifier handler"
  ],
  [
    "KWP_0x33_RoutineResults",
    8543922,
    "f",
    "KWP2000 SID 0x33 RequestRoutineResultsByLocalIdentifier handler"
  ],
  [
    "KWP_0x34_36_37_ModeGate",
    8527268,
    "f",
    "KWP2000 SID 0x34/0x36/0x37 upload/download mode gate"
  ],
  [
    "KWP_MaskROM_Bridge",
    8526502,
    "f",
    "KWP2000 flash-to-MaskROM bridge trampoline"
  ],
  [
    "KWP_SID_IndexTable",
    8506866,
    "l",
    "KWP2000 service ID (SID) index lookup table"
  ],
  [
    "KWP_Handler_Table",
    8506730,
    "l",
    "KWP2000 service handler jump/pointer table"
  ],
  [
    "KWP_LFSR_PolyTable",
    8510680,
    "l",
    "KWP2000 SecurityAccess LFSR polynomial table"
  ],
  [
    "Boot_Magic_Check",
    8437456,
    "f",
    "Bootloader / startup magic word check"
  ],
  [
    "Overrun_KFTVSA_Timer",
    8832320,
    "f",
    "Overrun fuel-cut delay timer consumer (KFTVSA -> RAM A24E)"
  ],
  [
    "Overrun_Zwmin_Floor",
    8897206,
    "f",
    "Overrun / minimum ignition angle floor stage"
  ],
  [
    "KFSU_Intake_Flap",
    8788096,
    "f",
    "Intake resonance flap (Saugrohrumschaltung / KFSU) control"
  ],
  [
    "LAMFA_Lookup",
    8809038,
    "f",
    "Driver-requested lambda (LAMFA) table lookup"
  ],
  [
    "KFMIRL_Lookup",
    8786304,
    "f",
    "Target cylinder charge from torque (KFMIRL) lookup"
  ],
  [
    "KFMSNWDK_Lookup_1",
    8776242,
    "f",
    "Normalized throttle mass flow (KFMSNWDK) lookup site 1"
  ],
  [
    "KFMSNWDK_Lookup_2",
    8791918,
    "f",
    "Normalized throttle mass flow (KFMSNWDK) lookup site 2"
  ],
  [
    "KFWDKMSN_TargetAngle",
    8785014,
    "f",
    "Target throttle plate angle (KFWDKMSN) computation"
  ],
  [
    "WDC_Gate_50F2h",
    8772528,
    "f",
    "Throttle/torque plausibility gate (RAM 50F2h)"
  ],
  [
    "KFPED_ModeSelect",
    8843226,
    "f",
    "Pedal map (KFPED) mode selector"
  ],
  [
    "KFPED_FullPedal",
    8845052,
    "f",
    "Full-pedal (KFPED) torque request lookup"
  ],
  [
    "KFZW_VarioCamBlend",
    8562192,
    "f",
    "KFZW / KFZW2 VarioCam ignition angle blend"
  ],
  [
    "Monitor_Param_Check",
    8700322,
    "f",
    "Function monitoring / plausibility parameter check"
  ],
  [
    "Map_19E30_Consumer",
    8808504,
    "f",
    "Consumer of calibration map at 0x819E30 (file 0x19E30)"
  ],
  [
    "FVERMN",
    8454169,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=- | eq=0.00390625 * X | Kennlinie Faktor Vermischung Regeneriergas Tankentl\u00fcftung mit Frischluft"
  ],
  [
    "FVERMN_x_axis",
    8454163,
    "l",
    "[VERIFIED_TUNER X-Axis for FVERMN] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "ETALAM",
    8454639,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x10 UBYTE] units=% | eq=0.5 * X | Lambda-Wirkungsgrad"
  ],
  [
    "ETALAM_x_axis",
    8454629,
    "l",
    "[VERIFIED_TUNER X-Axis for ETALAM] 10 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFZWOP1",
    8454714,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x16 SBYTE] units=deg BTDC | eq=0.75*X | Optimal Ignition Timing Surface 1 (Economy Advance / MBT)"
  ],
  [
    "KFZWOP1_x_axis",
    8455901,
    "l",
    "[VERIFIED_TUNER X-Axis for KFZWOP1] 16 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "KFZWOP1_y_axis",
    8455810,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFZWOP1] 16 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFZWOP2",
    8454970,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x16 SBYTE] units=deg BTDC | eq=0.75*X | Optimal Ignition Timing Surface 2 (VarioCam Active)"
  ],
  [
    "KFZWOP2_x_axis",
    8455901,
    "l",
    "[VERIFIED_TUNER X-Axis for KFZWOP2] 16 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "KFZWOP2_y_axis",
    8455810,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFZWOP2] 16 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFAFTE",
    8455384,
    "l",
    "[VERIFIED_TUNER MAP_3D 10x10 UBYTE] units=purge flow factor | eq=0.0078125*X | EVAP Tank Ventilation Purge Valve Flow Curve"
  ],
  [
    "KFAFTE_x_axis",
    8455364,
    "l",
    "[VERIFIED_TUNER X-Axis for KFAFTE] 10 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFAFTE_y_axis",
    8455374,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFAFTE] 10 pts UBYTE | units=wdkba (throttle %) | eq=X*100/255"
  ],
  [
    "LURBRL8",
    8455874,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=(Umdr./sec)^2 | eq=X | Laufunruhe-Referenzwert bei Fahrzeug steht"
  ],
  [
    "LURBRL8_x_axis",
    8455866,
    "l",
    "[VERIFIED_TUNER X-Axis for LURBRL8] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "WDKDSVLU",
    8456595,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=% DK | eq=X | Drosselklappenschwelle f\u00fcr Drucksensorplausibilisierung"
  ],
  [
    "WDKDSVLU_x_axis",
    8456589,
    "l",
    "[VERIFIED_TUNER X-Axis for WDKDSVLU] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFKSWF",
    8457023,
    "l",
    "[VERIFIED_TUNER MAP_3D 6x6 UBYTE] units= | eq=X | Kennfeld f\u00fcr Kat.-Schutz-Wichtungsfaktoren"
  ],
  [
    "KFKSWF_x_axis",
    8457011,
    "l",
    "[VERIFIED_TUNER X-Axis for KFKSWF] 6 pts UBYTE | units=nmot_ub_q40 | eq=40.0*X"
  ],
  [
    "KFKSWF_y_axis",
    8457017,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFKSWF] 6 pts UBYTE | units=rel_ub_q0p75 | eq=0.75*X"
  ],
  [
    "RLNOT",
    8457780,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=% | eq=X | Notlauf rl bei E_DK und E_LM"
  ],
  [
    "RLNOT_x_axis",
    8457774,
    "l",
    "[VERIFIED_TUNER X-Axis for RLNOT] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFKHFM",
    8457817,
    "l",
    "[VERIFIED_TUNER MAP_3D 14x14 UBYTE] units=factor | eq=0.0078125*X | HFM Airflow Correction Factor Map"
  ],
  [
    "KFKHFM_x_axis",
    8457789,
    "l",
    "[VERIFIED_TUNER X-Axis for KFKHFM] 14 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFKHFM_y_axis",
    8457803,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFKHFM] 14 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "KFPU",
    8458043,
    "l",
    "[VERIFIED_TUNER MAP_3D 14x14 UBYTE] units=factor | eq=0.0078125*X | Exhaust / Intake Pulsation Correction Map 1"
  ],
  [
    "KFPU_x_axis",
    8458015,
    "l",
    "[VERIFIED_TUNER X-Axis for KFPU] 14 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFPU_y_axis",
    8458029,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFPU] 14 pts UBYTE | units=wdkba (% throttle) | eq=X*100/255"
  ],
  [
    "KFPUSUVS",
    8458269,
    "l",
    "[VERIFIED_TUNER MAP_3D 14x14 UBYTE] units=- | eq=0.0078125 * X | Pulsationskennfeld bei aktiver Saugrohrumschaltung und gro\u00dfem Ventilhub"
  ],
  [
    "KFPUSUVS_x_axis",
    8458241,
    "l",
    "[VERIFIED_TUNER X-Axis for KFPUSUVS] 14 pts UBYTE | units=nmot_ub_q40 | eq=40.0*X"
  ],
  [
    "KFPUSUVS_y_axis",
    8458255,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFPUSUVS] 14 pts UBYTE | units=relDK_ub_b100 | eq=0.392157*X"
  ],
  [
    "KFPUSU",
    8458495,
    "l",
    "[VERIFIED_TUNER MAP_3D 14x14 UBYTE] units=factor | eq=0.0078125*X | Air Pulsation Correction Map with Intake Flap Open"
  ],
  [
    "KFPUSU_x_axis",
    8458467,
    "l",
    "[VERIFIED_TUNER X-Axis for KFPUSU] 14 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFPUSU_y_axis",
    8458481,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFPUSU] 14 pts UBYTE | units=wdkba (% throttle) | eq=X*100/255"
  ],
  [
    "KFPUVS",
    8458721,
    "l",
    "[VERIFIED_TUNER MAP_3D 14x14 UBYTE] units=factor | eq=0.0078125*X | Air Pulsation Correction Map Variant 4"
  ],
  [
    "KFPUVS_x_axis",
    8458693,
    "l",
    "[VERIFIED_TUNER X-Axis for KFPUVS] 14 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFPUVS_y_axis",
    8458707,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFPUVS] 14 pts UBYTE | units=wdkba (% throttle) | eq=X*100/255"
  ],
  [
    "TVLLRI",
    8460292,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=s | eq=0.02 * X | Verz\u00f6gerungszeit f\u00fcr Freigabe I-Anteil nach Start"
  ],
  [
    "TVLLRI_x_axis",
    8460286,
    "l",
    "[VERIFIED_TUNER X-Axis for TVLLRI] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "FDARTM",
    8460357,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=- | eq=X | Wichtungsfaktor Motortemperatur"
  ],
  [
    "FDARTM_x_axis",
    8460351,
    "l",
    "[VERIFIED_TUNER X-Axis for FDARTM] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "FSWALUV",
    8461547,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x4 UBYTE] units=m/(s^2) | eq=0.217 * X | Erkennungsschwelle Schlechtwegstrecke abh\u00e4ngig von Fz.geschwindigkeit"
  ],
  [
    "FSWALUV_x_axis",
    8461543,
    "l",
    "[VERIFIED_TUNER X-Axis for FSWALUV] 4 pts UBYTE | units=- | eq=X"
  ],
  [
    "FLRM",
    8461559,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x5 UBYTE] units=- | eq=0.015625 * X | Faktor f\u00fcr I-Dynamik des Lambdareglers in Abh\u00e4ngigkeit von tmot"
  ],
  [
    "FLRM_x_axis",
    8461554,
    "l",
    "[VERIFIED_TUNER X-Axis for FLRM] 5 pts UBYTE | units=- | eq=X"
  ],
  [
    "TSPERN",
    8461574,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x7 UBYTE] units=s | eq=0.01 * X | Sperrzeit P-Sprung nach Sondensprung"
  ],
  [
    "TSPERN_x_axis",
    8461567,
    "l",
    "[VERIFIED_TUNER X-Axis for TSPERN] 7 pts UBYTE | units=- | eq=X"
  ],
  [
    "TSPERN2",
    8461589,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x7 UBYTE] units=s | eq=0.01 * X | Sperrzeit P-Sprung nach Sondensprung, Bank 2"
  ],
  [
    "TSPERN2_x_axis",
    8461582,
    "l",
    "[VERIFIED_TUNER X-Axis for TSPERN2] 7 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFZW",
    8461664,
    "l",
    "[VERIFIED_TUNER MAP_3D 24x16 SBYTE] units=deg BTDC | eq=0.75*X | Primary Ignition Timing Base Map (WOT / Part Load)"
  ],
  [
    "KFZW_x_axis",
    8455901,
    "l",
    "[VERIFIED_TUNER X-Axis for KFZW] 16 pts UBYTE | units=rlkr (load %) | eq=0.75*X"
  ],
  [
    "KFZW_y_axis",
    8455827,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFZW] 24 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFZW2",
    8462048,
    "l",
    "[VERIFIED_TUNER MAP_3D 24x16 SBYTE] units=deg BTDC | eq=0.75*X | Ignition Timing Map Variant 2 (VarioCam Cam Advance Active)"
  ],
  [
    "KFZW2_x_axis",
    8455901,
    "l",
    "[VERIFIED_TUNER X-Axis for KFZW2] 16 pts UBYTE | units=rlkr (load %) | eq=0.75*X"
  ],
  [
    "KFZW2_y_axis",
    8455827,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFZW2] 24 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFZWMN",
    8462432,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x12 SBYTE] units=deg BTDC | eq=0.75*X | Minimum Ignition Timing Floor (Knock Retard Limit)"
  ],
  [
    "KFZWMN_x_axis",
    8455888,
    "l",
    "[VERIFIED_TUNER X-Axis for KFZWMN] 12 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "KFZWMN_y_axis",
    8455810,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFZWMN] 16 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFZWMS",
    8462816,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x12 SBYTE] units=deg BTDC | eq=0.75*X | Permanent Maximum Retarded Ignition Timing Boundary"
  ],
  [
    "KFZWMS_x_axis",
    8455888,
    "l",
    "[VERIFIED_TUNER X-Axis for KFZWMS] 12 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "KFZWMS_y_axis",
    8455810,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFZWMS] 16 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KOPWMTU",
    8463033,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units= | eq=X | Nachbildung Kompressor-Last aus Umgebungstemperatur"
  ],
  [
    "KOPWMTU_x_axis",
    8463025,
    "l",
    "[VERIFIED_TUNER X-Axis for KOPWMTU] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "DZWOM",
    8471408,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x5 UBYTE] units=grad KW | eq=X | temperaturabh\u00e4ngiger Offset des optimalen ZW"
  ],
  [
    "DZWOM_x_axis",
    8471403,
    "l",
    "[VERIFIED_TUNER X-Axis for DZWOM] 5 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFMIOP",
    8471414,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x16 UWORD] units=% optimal torque | eq=0.0015258789*X | Optimal Engine Torque Map (Inverse Model)"
  ],
  [
    "KFMIOP_x_axis",
    8455901,
    "l",
    "[VERIFIED_TUNER X-Axis for KFMIOP] 16 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "KFMIOP_y_axis",
    8455810,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFMIOP] 16 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFMSNWDK",
    8475010,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x6 UWORD] units=kg/h | eq=0.1*X | Normalized Air Mass Flow Over Throttle Body (BGMSZS)"
  ],
  [
    "KFMSNWDK_x_axis",
    8474998,
    "l",
    "[VERIFIED_TUNER X-Axis for KFMSNWDK] 6 pts UWORD | units=nmot (RPM) | eq=0.25*X"
  ],
  [
    "KFMSNWDK_y_axis",
    8474966,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFMSNWDK] 16 pts UWORD | units=wdkba (throttle %) | eq=0.0015259022*X"
  ],
  [
    "KLAF",
    8475202,
    "l",
    "[VERIFIED_TUNER CURVE_1D 1x501 UWORD] units=outflow factor | eq=X/65536 | Throttle Body Discharge Outflow Characteristic (501 Points)"
  ],
  [
    "MLHFM",
    8476308,
    "l",
    "[VERIFIED_TUNER CURVE_1D 1x512 UWORD] units=kg/h | eq=0.1*X | MAF Sensor 512-Point Voltage Linearization Curve"
  ],
  [
    "KFWDKMSN",
    8477448,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x6 UWORD] units=% throttle angle | eq=X*100/65535 | Target Throttle Plate Angle from Demanded Airflow"
  ],
  [
    "KFWDKMSN_x_axis",
    8477436,
    "l",
    "[VERIFIED_TUNER X-Axis for KFWDKMSN] 6 pts UWORD | units=nmot (RPM) | eq=0.25*X"
  ],
  [
    "KFWDKMSN_y_axis",
    8477404,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFWDKMSN] 16 pts UWORD | units=msndko (norm flow) | eq=0.1*X"
  ],
  [
    "KFMIRL",
    8477766,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x16 UWORD] units=Load % fill | eq=0.0234375*X | Engine Load Fill Target from Requested Torque"
  ],
  [
    "KFMIRL_x_axis",
    8477734,
    "l",
    "[VERIFIED_TUNER X-Axis for KFMIRL] 16 pts UWORD | units=misopl (% torque) | eq=0.0015258789*X"
  ],
  [
    "KFMIRL_y_axis",
    8477702,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFMIRL] 16 pts UWORD | units=nmot (RPM) | eq=0.25*X"
  ],
  [
    "KFMDS",
    8479208,
    "l",
    "[VERIFIED_TUNER MAP_3D 12x10 UWORD] units=% drag torque | eq=0.0015259022*X | Engine Mechanical Drag & Friction Torque Loss Model"
  ],
  [
    "KFMDS_x_axis",
    8479164,
    "l",
    "[VERIFIED_TUNER X-Axis for KFMDS] 10 pts UWORD | units=nmot_w (RPM) | eq=0.25*X"
  ],
  [
    "KFMDS_y_axis",
    8479184,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFMDS] 12 pts UWORD | units=rl_w (load %) | eq=0.0234375*X"
  ],
  [
    "KFPED",
    8479852,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x13 UWORD] units=% demanded torque | eq=X*200/65535 | Driver Demanded Torque vs Accelerator Pedal Position"
  ],
  [
    "KFPED_x_axis",
    8479826,
    "l",
    "[VERIFIED_TUNER X-Axis for KFPED] 13 pts UWORD | units=nmot (RPM) | eq=0.25*X"
  ],
  [
    "KFPED_y_axis",
    8479794,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFPED] 16 pts UWORD | units=wped (pedal %) | eq=0.0015259*X"
  ],
  [
    "KFPEDR",
    8480320,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x8 UWORD] units=% demanded torque | eq=X*200/65535 | Driver Demanded Torque in Reverse Gear"
  ],
  [
    "KFPEDR_x_axis",
    8480304,
    "l",
    "[VERIFIED_TUNER X-Axis for KFPEDR] 8 pts UWORD | units=nmot (RPM) | eq=0.25*X"
  ],
  [
    "KFPEDR_y_axis",
    8480272,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFPEDR] 16 pts UWORD | units=wped (pedal %) | eq=0.0015259*X"
  ],
  [
    "NMAX",
    8480604,
    "l",
    "[VERIFIED_TUNER SCALAR 1x1 UWORD] units=rpm | eq=0.25*X | Primary Rev Limiter Threshold (NMAX)"
  ],
  [
    "NMAXOG",
    8480606,
    "l",
    "[VERIFIED_TUNER SCALAR 1x1 UWORD] units=rpm | eq=0.25*X | Upper Rev Limiter Threshold (NMAXOG)"
  ],
  [
    "DWVLSN",
    8480976,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x7 UBYTE] units=grad KW | eq=X | Delta - Z\u00fcndwinkel Vollast sp\u00e4t Motorschutz"
  ],
  [
    "DWVLSN_x_axis",
    8480969,
    "l",
    "[VERIFIED_TUNER X-Axis for DWVLSN] 7 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFRLIP_UM",
    8485668,
    "l",
    "[VERIFIED_TUNER MAP_3D 8x8 UBYTE] units=% | eq=X | Kennfeld f\u00fcr rl - Berechnung aus Drosselklappenwinkel in der Funktions\u00fcberwachg"
  ],
  [
    "KFRLIP_UM_x_axis",
    8485652,
    "l",
    "[VERIFIED_TUNER X-Axis for KFRLIP_UM] 8 pts UBYTE | units=spg_ub_q0p019 | eq=0.019531*X"
  ],
  [
    "KFRLIP_UM_y_axis",
    8485660,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFRLIP_UM] 8 pts UBYTE | units=nmot_ub_q40 | eq=40.0*X"
  ],
  [
    "WDKSNLN",
    8485767,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=% DK | eq=X | Sollwinkel f\u00fcr Drosselklappe bei Kl15 aus"
  ],
  [
    "WDKSNLN_x_axis",
    8485759,
    "l",
    "[VERIFIED_TUNER X-Axis for WDKSNLN] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "FVSTMKG",
    8485922,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=- | eq=0.00390625 * X | Gemischkorrektur Tmot-Abh\u00e4ngig bei VS von klein nach gro\u00df"
  ],
  [
    "FVSTMKG_x_axis",
    8485914,
    "l",
    "[VERIFIED_TUNER X-Axis for FVSTMKG] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "TVLLRPD",
    8491255,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=s | eq=0.02 * X | Maximale Verz\u00f6gerungszeit f\u00fcr Freigabe PD-Anteil nach Start"
  ],
  [
    "TVLLRPD_x_axis",
    8491249,
    "l",
    "[VERIFIED_TUNER X-Axis for TVLLRPD] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "FBTEB",
    8491269,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=- | eq=0.00390625 * X | Faktor Begrenzung Lerngeschwindigkeit f\u00fcr Beladung"
  ],
  [
    "FBTEB_x_axis",
    8491263,
    "l",
    "[VERIFIED_TUNER X-Axis for FBTEB] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "FETATEBN",
    8491294,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x5 UBYTE] units=- | eq=0.00390625 * X | Kennlinie f\u00fcr drehzahlabh\u00e4ngigen Sollwert des Motorwirkungsgrades"
  ],
  [
    "FETATEBN_x_axis",
    8491289,
    "l",
    "[VERIFIED_TUNER X-Axis for FETATEBN] 5 pts UBYTE | units=- | eq=X"
  ],
  [
    "FQTEVA",
    8491306,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=- | eq=0.0625 * X | Progression bei Sp\u00fclratenaufsteuerung"
  ],
  [
    "FQTEVA_x_axis",
    8491300,
    "l",
    "[VERIFIED_TUNER X-Axis for FQTEVA] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "FTEINIX",
    8491323,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x5 UBYTE] units=- | eq=0.001953125 * X | Kennlinie Max. Sp\u00fclrate abh\u00e4ngig vom Integral Massenstrom TE nach TE Stop"
  ],
  [
    "FTEINIX_x_axis",
    8491318,
    "l",
    "[VERIFIED_TUNER X-Axis for FTEINIX] 5 pts UBYTE | units=- | eq=X"
  ],
  [
    "FLTEFUEL",
    8491679,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x4 UBYTE] units=- | eq=0.00390625 * X | Faktor Anteil TEV Strom, der direkt ins Saugrohr str\u00f6mt"
  ],
  [
    "FLTEFUEL_x_axis",
    8491675,
    "l",
    "[VERIFIED_TUNER X-Axis for FLTEFUEL] 4 pts UBYTE | units=- | eq=X"
  ],
  [
    "TVSUNA",
    8493056,
    "l",
    "[VERIFIED_TUNER VALUE 1x1 UBYTE] units=s | eq=0.05 * X | Verz\u00f6gerungszeit f\u00fcr Saugrohrumschaltung, wenn nicht angesteuert"
  ],
  [
    "FMSML",
    8491851,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=- | eq=0.0078125 * X | Abgasgegendruckkorrektur der Sekund\u00e4rluftmasse"
  ],
  [
    "FMSML_x_axis",
    8491843,
    "l",
    "[VERIFIED_TUNER X-Axis for FMSML] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "MSLUB",
    8491888,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=kg | eq=X | Sekund\u00e4rluftmasse abh\u00e4ngig von der Batteriespannung"
  ],
  [
    "MSLUB_x_axis",
    8491880,
    "l",
    "[VERIFIED_TUNER X-Axis for MSLUB] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFTPKOR",
    8492505,
    "l",
    "[VERIFIED_TUNER MAP_3D 7x8 UBYTE] units=factor | eq=0.0078125*X | Rough Road & Misfire Detection TP Period Correction"
  ],
  [
    "KFTPKOR_x_axis",
    8492489,
    "l",
    "[VERIFIED_TUNER X-Axis for KFTPKOR] 8 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFTPKOR_y_axis",
    8492498,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFTPKOR] 7 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "FDVANS",
    8492668,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=- | eq=0.0078125 * X | Temperaturfaktor f\u00fcr Drosselventildurchflu\u00df"
  ],
  [
    "FDVANS_x_axis",
    8492660,
    "l",
    "[VERIFIED_TUNER X-Axis for FDVANS] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFSU",
    8492948,
    "l",
    "[VERIFIED_TUNER MAP_3D 6x6 UBYTE] units=state (0=Shut, 1=Hold, 2=Open) | eq=X | Intake Manifold Resonance Flap 1 Schedule"
  ],
  [
    "KFSU_x_axis",
    8492936,
    "l",
    "[VERIFIED_TUNER X-Axis for KFSU] 6 pts UBYTE | units=temp_su_nmot (RPM) | eq=40*X"
  ],
  [
    "KFSU_y_axis",
    8492942,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFSU] 6 pts UBYTE | units=rlshk (load %) | eq=0.75*X"
  ],
  [
    "KFSU2",
    8492998,
    "l",
    "[VERIFIED_TUNER MAP_3D 6x6 UBYTE] units=state (disabled/zeros) | eq=X | Intake Manifold Resonance Flap 2 (Disabled / Zeroed)"
  ],
  [
    "KFSU2_x_axis",
    8492986,
    "l",
    "[VERIFIED_TUNER X-Axis for KFSU2] 6 pts UBYTE | units=temp_su_nmot (RPM) | eq=40*X"
  ],
  [
    "KFSU2_y_axis",
    8492992,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFSU2] 6 pts UBYTE | units=rlshk (load %) | eq=0.75*X"
  ],
  [
    "FWET",
    8493680,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x9 UBYTE] units=- | eq=0.0078125 * X | Faktor Wiedereinsetzmenge temperaturabhaengig"
  ],
  [
    "FWET_x_axis",
    8493671,
    "l",
    "[VERIFIED_TUNER X-Axis for FWET] 9 pts UBYTE | units=- | eq=X"
  ],
  [
    "FQTEDL",
    8494237,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x5 UBYTE] units=- | eq=X | Kennlinie Faktor f\u00fcr exponentielle Absteuerung Sp\u00fclrate"
  ],
  [
    "FQTEDL_x_axis",
    8494232,
    "l",
    "[VERIFIED_TUNER X-Axis for FQTEDL] 5 pts UBYTE | units=- | eq=X"
  ],
  [
    "WDKARN",
    8494914,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x10 UBYTE] units=% DK | eq=0.39215686274509803 * X | DK-Winkel-Schwelle f\u00fcr Gemischadaption aktiv"
  ],
  [
    "WDKARN_x_axis",
    8494904,
    "l",
    "[VERIFIED_TUNER X-Axis for WDKARN] 10 pts UBYTE | units=- | eq=X"
  ],
  [
    "TMRELI",
    8495082,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x15 UBYTE] units=Grad C | eq=0.75 * X + -48.0 | Temperatur Motorraum, Erfassung u. Linearisierung, Inverskennlinie"
  ],
  [
    "TMRELI_x_axis",
    8495067,
    "l",
    "[VERIFIED_TUNER X-Axis for TMRELI] 15 pts UBYTE | units=- | eq=X"
  ],
  [
    "MLSUS",
    8495183,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x12 UBYTE] units=kg | eq=0.022755555555555557 * X | Sollwert Luftmassen-Integral f\u00fcr motorisches Katheizen"
  ],
  [
    "MLSUS_x_axis",
    8495171,
    "l",
    "[VERIFIED_TUNER X-Axis for MLSUS] 12 pts UBYTE | units=- | eq=X"
  ],
  [
    "LASTMOT",
    8495415,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x4 UBYTE] units=- | eq=0.0078125 * X | Motortemp.-Korrektur von Lambda-Abgas-Soll"
  ],
  [
    "LASTMOT_x_axis",
    8495411,
    "l",
    "[VERIFIED_TUNER X-Axis for LASTMOT] 4 pts UBYTE | units=- | eq=X"
  ],
  [
    "FABMDWA",
    8495872,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=- | eq=0.00390625 * X | Faktor zur Absteuerung des Wandlermoments abh\u00e4ngig von nturb/nsol"
  ],
  [
    "FABMDWA_x_axis",
    8495866,
    "l",
    "[VERIFIED_TUNER X-Axis for FABMDWA] 6 pts UBYTE | units=- | eq=X"
  ],
  [
    "TVZWVS1",
    8495935,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=s | eq=0.02 * X | Einschaltverz\u00f6gerung ZW-Einflu\u00df bei Ventilhubumschaltung"
  ],
  [
    "TVZWVS1_x_axis",
    8495927,
    "l",
    "[VERIFIED_TUNER X-Axis for TVZWVS1] 8 pts UBYTE | units=- | eq=X"
  ],
  [
    "KFTEKA",
    8497124,
    "l",
    "[VERIFIED_TUNER MAP_3D 5x5 UBYTE] units=- | eq=0.0078125 * X | Kennfeld Sollkraftstoffanteil bei Regenerierung"
  ],
  [
    "KFTEKA_x_axis",
    8497114,
    "l",
    "[VERIFIED_TUNER X-Axis for KFTEKA] 5 pts UBYTE | units=nmot_ub_q40 | eq=40.0*X"
  ],
  [
    "KFTEKA_y_axis",
    8497119,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFTEKA] 5 pts UBYTE | units=rel_ub_q0p75 | eq=0.75*X"
  ],
  [
    "TVSUM",
    8493050,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x6 UBYTE] units=s | eq=X | Zeitverz\u00f6gerung der Saugrohrumschaltung in Abh\u00e4ngigkeit von der Motortemperatur"
  ],
  [
    "TVSUM_x_axis",
    8493044,
    "l",
    "[VERIFIED_TUNER X-Axis for TVSUM] 6 pts UBYTE | units=tmot | eq=0.75*X-48"
  ],
  [
    "LAMFA",
    8500272,
    "l",
    "[VERIFIED_TUNER MAP_3D 13x6 UBYTE] units=Lambda | eq=0.0078125*X | Driver-Demanded Target Lambda Map (Full Throttle Enrichment)"
  ],
  [
    "LAMFA_x_axis",
    8500260,
    "l",
    "[VERIFIED_TUNER X-Axis for LAMFA] 6 pts UWORD | units=mrfa / load (%) | eq=0.0030517578*X"
  ],
  [
    "LAMFA_y_axis",
    8500246,
    "l",
    "[VERIFIED_TUNER Y-Axis for LAMFA] 13 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFDTMTE",
    8501539,
    "l",
    "[VERIFIED_TUNER MAP_3D 4x5 UBYTE] units=Grad C | eq=0.000732421875 * X | Kennfeld Motortemperaturgradient f\u00fcr Ersatztemperatur"
  ],
  [
    "KFDTMTE_x_axis",
    8501529,
    "l",
    "[VERIFIED_TUNER X-Axis for KFDTMTE] 5 pts UBYTE | units=m_ub_b1020 | eq=4.0*X"
  ],
  [
    "KFDTMTE_y_axis",
    8501535,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFDTMTE] 4 pts UBYTE | units=temp_ub_q0p75_o48 | eq=0.75*X-48.0"
  ],
  [
    "KFDTMTR",
    8501571,
    "l",
    "[VERIFIED_TUNER MAP_3D 4x5 UBYTE] units=Grad C | eq=0.000732421875 * X | Kennfeld Motortemperaturgradient f\u00fcr Referenztemperatur"
  ],
  [
    "KFDTMTR_x_axis",
    8501561,
    "l",
    "[VERIFIED_TUNER X-Axis for KFDTMTR] 5 pts UBYTE | units=m_ub_b1020 | eq=4.0*X"
  ],
  [
    "KFDTMTR_y_axis",
    8501567,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFDTMTR] 4 pts UBYTE | units=temp_ub_q0p75_o48 | eq=0.75*X-48.0"
  ],
  [
    "WDKPMXN",
    8503030,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x12 UBYTE] units=% DK | eq=0.39215686274509803 * X | Maximaler Drosselklappenwinkel f\u00fcr Plausibilisierung mit F\u00fcllungssignal"
  ],
  [
    "WDKPMXN_x_axis",
    8503018,
    "l",
    "[VERIFIED_TUNER X-Axis for WDKPMXN] 12 pts UBYTE | units=- | eq=X"
  ],
  [
    "NKTOLVS",
    8455754,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x8 UBYTE] units=- | eq=40 * X | Drehzahlkorrektur f\u00fcr Schaltschwellen in Abh\u00e4ngigkeit von Tol"
  ],
  [
    "NKTOLVS_x_axis",
    8455746,
    "l",
    "[VERIFIED_TUNER X-Axis for NKTOLVS] 8 pts UBYTE | units=tol | eq=0.75 * X - 48"
  ],
  [
    "RLVMXN",
    8496105,
    "l",
    "[VERIFIED_TUNER CURVE_2D 1x11 UBYTE] units=- | eq=0.75 * X | Maximaler Volumenstrom bei offener Drosselklappe"
  ],
  [
    "RLVMXN_x_axis",
    8496094,
    "l",
    "[VERIFIED_TUNER X-Axis for RLVMXN] 11 pts UBYTE | units=nmot | eq=40 * X"
  ],
  [
    "KFZWMNX",
    8462624,
    "l",
    "[VERIFIED_TUNER MAP_3D 16x12 SBYTE] units=deg BTDC | eq=0.75*X | Alternate Minimum Ignition Timing Floor (Blended with KFZWMN)"
  ],
  [
    "KFZWMNX_x_axis",
    8455888,
    "l",
    "[VERIFIED_TUNER X-Axis for KFZWMNX] 12 pts UBYTE | units=rl (load %) | eq=0.75*X"
  ],
  [
    "KFZWMNX_y_axis",
    8455810,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFZWMNX] 16 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFTVSA",
    8495798,
    "l",
    "[VERIFIED_TUNER MAP_3D 5x8 UBYTE] units=s | eq=0.01*X | Overrun Fuel-Cut Delay Time (tmot x nmot)"
  ],
  [
    "KFTVSA_x_axis",
    8455764,
    "l",
    "[VERIFIED_TUNER X-Axis for KFTVSA] 8 pts UBYTE | units=nmot (RPM) | eq=40*X"
  ],
  [
    "KFTVSA_y_axis",
    8491701,
    "l",
    "[VERIFIED_TUNER Y-Axis for KFTVSA] 5 pts UBYTE | units=tmot (deg C) | eq=0.75*X-48"
  ],
  [
    "nmot_w",
    63554,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.25 rpm"
  ],
  [
    "nmot",
    63552,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 40 rpm"
  ],
  [
    "rl_w",
    63576,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.0234375 %"
  ],
  [
    "rl_w_mirror_3809AA",
    3672490,
    "l",
    "[CONFIRMED_RAM_MIRROR of rl_w @ 0x00F858] UWORD 2B | formula=x * 0.0234375 %"
  ],
  [
    "rl",
    3672889,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.75 %"
  ],
  [
    "mshfm_w",
    63572,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.1 kg/h"
  ],
  [
    "mshfm_w_mirror_3809A6",
    3672486,
    "l",
    "[CONFIRMED_RAM_MIRROR of mshfm_w @ 0x00F854] UWORD 2B | formula=x * 0.1 kg/h"
  ],
  [
    "ps_w",
    63574,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.0390625 hPa"
  ],
  [
    "zwout",
    63561,
    "l",
    "[CONFIRMED_RAM SBYTE 1B] formula=signed x * 0.75 \u00b0KW (positive = advance / BTDC); OBD PID 0E encoding unknown"
  ],
  [
    "zwout_mirror_3809AC",
    3672492,
    "l",
    "[CONFIRMED_RAM_MIRROR of zwout @ 0x00F849] SBYTE 1B | formula=signed x * 0.75 \u00b0KW (positive = advance / BTDC); OBD PID 0E encoding unknown"
  ],
  [
    "zwgru",
    63560,
    "l",
    "[CONFIRMED_RAM SBYTE 1B] formula=x * 0.75 \u00b0KW"
  ],
  [
    "tmot",
    3672942,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.75 - 48 \u00b0C"
  ],
  [
    "toil",
    3672956,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.75 - 48 \u00b0C"
  ],
  [
    "tans",
    3672672,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.75 - 48 \u00b0C"
  ],
  [
    "tmot_raum",
    3672940,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.75 - 48 \u00b0C"
  ],
  [
    "tkat",
    3672777,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 5 - 50 \u00b0C"
  ],
  [
    "tabgm",
    3672768,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 5 - 50 \u00b0C"
  ],
  [
    "ub",
    3672636,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.0704 V"
  ],
  [
    "ub_mirror_3809AB",
    3672491,
    "l",
    "[CONFIRMED_RAM_MIRROR of ub @ 0x380A3C] UBYTE 1B | formula=x * 0.0704 V"
  ],
  [
    "wdkba_w",
    63688,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.0015259 %"
  ],
  [
    "wdkba",
    3673023,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.390625 %"
  ],
  [
    "wdkba_mirror_3809AD",
    3672493,
    "l",
    "[CONFIRMED_RAM_MIRROR of wdkba @ 0x380BBF] UBYTE 1B | formula=x * 0.390625 %"
  ],
  [
    "vfzg_b",
    3672612,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 1.25 km/h"
  ],
  [
    "vfzg_obd_b",
    3672763,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 1 km/h"
  ],
  [
    "fra1_b",
    3672746,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.78125 - 100 %"
  ],
  [
    "fra2_b",
    3672745,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.78125 - 100 %"
  ],
  [
    "fr1_b",
    3672747,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.78125 - 100 %"
  ],
  [
    "fr2_b",
    3672744,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.78125 - 100 %"
  ],
  [
    "adc_tmot",
    3672400,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 1 raw"
  ],
  [
    "adc_tans",
    3672399,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 1 raw"
  ],
  [
    "mshfm_obd_w",
    3678212,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.1 kg/h (x/3600 g/s)"
  ],
  [
    "rl_obd_w",
    3678218,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 100 / 65535 %"
  ],
  [
    "tmot_lin",
    3672935,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.75 - 48 \u00b0C"
  ],
  [
    "tans_lin",
    3672933,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * 0.75 - 48 \u00b0C"
  ],
  [
    "fr_w",
    3678994,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=(x - 32768) / 327.68 %"
  ],
  [
    "fr2_staging_w",
    3678996,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=(x - 32768) / 327.68 %"
  ],
  [
    "rkat_w",
    3679004,
    "l",
    "[CONFIRMED_RAM SWORD 2B] formula=signed x * 0.0061035 %"
  ],
  [
    "rkat2_staging_w",
    3679006,
    "l",
    "[CONFIRMED_RAM SWORD 2B] formula=signed x * 0.0061035 %"
  ],
  [
    "fra_w",
    3678238,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=(x - 32768) / 327.68 %"
  ],
  [
    "fra2_staging_w",
    3678240,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=(x - 32768) / 327.68 %"
  ],
  [
    "wkra",
    3672630,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=x * -0.75 \u00b0KW (6-byte block, one byte per cylinder 1-6)"
  ],
  [
    "nmot_kwp_w",
    3672476,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.25 RPM (claimed, UNVERIFIED)"
  ],
  [
    "vfzg_w",
    3672478,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 0.0078125 km/h (claimed, UNVERIFIED)"
  ],
  [
    "wped_w",
    3672484,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 100 / 65535 % (claimed, UNVERIFIED)"
  ],
  [
    "misol_w",
    63558,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x * 100 / 65536 %"
  ],
  [
    "fra1_w",
    3678592,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x / 32768.0"
  ],
  [
    "fra1_w_mirror_3838EA",
    3684586,
    "l",
    "[CONFIRMED_RAM_MIRROR of fra1_w @ 0x382180] UWORD 2B | formula=x / 32768.0"
  ],
  [
    "fra2_w",
    3678590,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x / 32768.0"
  ],
  [
    "fra2_w_mirror_3838E8",
    3684584,
    "l",
    "[CONFIRMED_RAM_MIRROR of fra2_w @ 0x38217E] UWORD 2B | formula=x / 32768.0"
  ],
  [
    "rkat1_w",
    3684590,
    "l",
    "[CONFIRMED_RAM SWORD 2B] formula=signed x * 0.046875 %"
  ],
  [
    "rkat2_w",
    3684588,
    "l",
    "[CONFIRMED_RAM SWORD 2B] formula=signed x * 0.046875 %"
  ],
  [
    "fr1_w",
    3679662,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x / 32768.0"
  ],
  [
    "fr1_w_mirror_3825A8",
    3679656,
    "l",
    "[CONFIRMED_RAM_MIRROR of fr1_w @ 0x3825AE] UWORD 2B | formula=x / 32768.0"
  ],
  [
    "fr2_w",
    3679644,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x / 32768.0"
  ],
  [
    "fr2_w_mirror_3825A6",
    3679654,
    "l",
    "[CONFIRMED_RAM_MIRROR of fr2_w @ 0x38259C] UWORD 2B | formula=x / 32768.0"
  ],
  [
    "tbtrnxo",
    3685244,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x / 10.0 h"
  ],
  [
    "tbtrnxo_mirror_382FBA",
    3682234,
    "l",
    "[CONFIRMED_RAM_MIRROR of tbtrnxo @ 0x383B7C] UWORD 2B | formula=x / 10.0 h"
  ],
  [
    "tbtrnxu",
    3685246,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x / 10.0 h"
  ],
  [
    "tbtrnxu_mirror_382FB8",
    3682232,
    "l",
    "[CONFIRMED_RAM_MIRROR of tbtrnxu @ 0x383B7E] UWORD 2B | formula=x / 10.0 h"
  ],
  [
    "nnmaxo",
    3685248,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x ignitions"
  ],
  [
    "nnmaxo_mirror_382FB6",
    3682230,
    "l",
    "[CONFIRMED_RAM_MIRROR of nnmaxo @ 0x383B80] UWORD 2B | formula=x ignitions"
  ],
  [
    "nnmaxu",
    3685250,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x ignitions"
  ],
  [
    "nnmaxu_mirror_382FB4",
    3682228,
    "l",
    "[CONFIRMED_RAM_MIRROR of nnmaxu @ 0x383B82] UWORD 2B | formula=x ignitions"
  ],
  [
    "topl_w",
    3685252,
    "l",
    "[CONFIRMED_RAM UWORD 2B] formula=x / 10.0 h"
  ],
  [
    "topl_w_mirror_382FAE",
    3682222,
    "l",
    "[CONFIRMED_RAM_MIRROR of topl_w @ 0x383B84] UWORD 2B | formula=x / 10.0 h"
  ],
  [
    "load_byte",
    63571,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "kftvsa_a24c",
    3678796,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "kftvsa_countdown_10ms",
    3678797,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "kftvsa_reload_latch",
    3678798,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "kftvsa_state_a254",
    3678804,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "kftvsa_capped_counter",
    3678806,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "f3_speed_branch_state",
    3674790,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "pedal_released_gate",
    64802,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "b_sa_fuel_cut_flag",
    64804,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "low_speed_delay_arm",
    64840,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "ce1..ce6",
    3673313,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "variocam_blend_weight",
    3673321,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "ced",
    3673325,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "cee",
    3673326,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "cef",
    3673327,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_front_b1_raw",
    3672559,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_front_b1_scaled",
    3672851,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_front_b2_raw",
    3672560,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_front_b2_scaled",
    3672852,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_rear_b1_raw",
    3673168,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_rear_b1_scaled",
    3672844,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_rear_b2_raw",
    3673169,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "o2_rear_b2_scaled",
    3672845,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "obd_pid03_fuel_status_b1",
    3673276,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "obd_pid03_fuel_status_b2",
    3673277,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "ti_candidate_b1",
    63432,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "wkra_0..5",
    3672630,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "load_scaled_correction_index",
    3674564,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "torque_gate_max_word",
    3679092,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "torque_gate_lut_result",
    3679094,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "e8e_live_channel",
    3677838,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "pedal_torque_latch",
    3679138,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "kfsu_flap_state_w",
    3678290,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "fzabg_w",
    3674078,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ],
  [
    "lur1..6_rough_running",
    3674082,
    "l",
    "[CONFIRMED_RAM UBYTE 1B] formula=X"
  ]
]


def run():
    listing = currentProgram.getListing()
    sym_table = currentProgram.getSymbolTable()
    seen_addrs = set()

    created_funcs = 0
    created_labels = 0
    skipped = 0

    for name, addr_int, kind, comment in SYMBOLS:
        addr = toAddr(addr_int)
        if not currentProgram.getMemory().contains(addr):
            printerr("Skipping %s @ 0x%06X: address not in program memory map (create IRAM/XRAM blocks first)." % (name, addr_int))
            skipped += 1
            continue

        is_primary = addr_int not in seen_addrs
        seen_addrs.add(addr_int)

        if kind == "f":
            func = getFunctionAt(addr)
            if func is None:
                disassemble(addr)
                func = createFunction(addr, name)
            if func is not None:
                if func.getName() != name:
                    func.setName(name, SourceType.USER_DEFINED)
                existing_plate = getPlateComment(addr)
                if not existing_plate:
                    setPlateComment(addr, comment)
                created_funcs += 1
            else:
                createLabel(addr, name, is_primary)
                setEOLComment(addr, comment)
                created_labels += 1
        else:
            existing = sym_table.getSymbols(addr)
            already_named = any(s.getName() == name for s in existing)
            if not already_named:
                createLabel(addr, name, is_primary)
            existing_eol = getEOLComment(addr)
            if not existing_eol:
                setEOLComment(addr, comment)
            elif comment not in existing_eol:
                setEOLComment(addr, existing_eol + " ; " + comment)
            created_labels += 1

    println("ME7.2 y966ohc import complete: %d functions, %d labels, %d skipped." % (created_funcs, created_labels, skipped))


run()
