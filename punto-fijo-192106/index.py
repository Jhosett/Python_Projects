import customtkinter as ctk

# Window--------------------------------------------------------------------------
ctk.set_appearance_mode("dark")
app = ctk.CTk()
app.geometry("1250x650")
app.title("Método de Punto Fijo - 192106")
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)
# --------------------------------------------------------------------------------

# Frames-------------------------------------------------------------------------
mainTab = ctk.CTkTabview(app)
calculateTab = mainTab.add("Calcular")
guideTab = mainTab.add("Guía")

mainTab.pack(pady=20, padx=20, fill="both", expand=True)
calculateTab.rowconfigure(0, weight=3)
calculateTab.rowconfigure(1, weight=1)
calculateTab.columnconfigure(0, weight=1)

# Guide Frames--------------------------------------------------------------------
guideFrame = ctk.CTkFrame(mainTab.tab("Guía"))
guideFrame.pack(pady=20, padx=20, fill="both", expand=True)


# Calculator Frames---------------------------------------------------------------
calculatorFrame = ctk.CTkFrame(mainTab.tab("Calcular"))
tableScrollableFrame = ctk.CTkScrollableFrame(calculatorFrame)
graphicFrame = ctk.CTkFrame(calculatorFrame)

commandFrame = ctk.CTkFrame(mainTab.tab("Calcular"))
inputFrame = ctk.CTkFrame(commandFrame)
padFrame = ctk.CTkFrame(commandFrame)

calculatorFrame.grid(row=0, column=0, sticky="nsew")
commandFrame.grid(row=1, column=0, sticky="nsew")

inputFrame.grid(row=0, column=0, sticky="nsew", padx=10)
padFrame.grid(row=0, column=1, sticky="nsew", padx=10)

commandFrame.columnconfigure(0, weight=2)
commandFrame.columnconfigure(1, weight=1)
commandFrame.rowconfigure(0, weight=1)

calculatorFrame.columnconfigure(0, weight=1)
calculatorFrame.columnconfigure(1, weight=1)
calculatorFrame.rowconfigure(0, weight=1)

# Input Frame---------------------------------------------------------------------
inputFunction = ctk.CTkEntry(inputFrame, placeholder_text="f(x) = ")
inputX0 = ctk.CTkEntry(inputFrame, placeholder_text="x0")
inputTolerance = ctk.CTkEntry(inputFrame, placeholder_text="Tolerancia")
calculateButton = ctk.CTkButton(inputFrame, text="Calcular")

inputFunction.pack(pady=10, padx=10, expand=True, fill="both")
inputX0.pack(pady=10, padx=10, expand=True, fill="both")
inputTolerance.pack(pady=10, padx=10, expand=True, fill="both")
calculateButton.pack(pady=10, padx=10, expand=True, fill="both")

calculateButton.configure(command=lambda: calculateFixedPoint())

# Pad Frame-----------------------------------------------------------------------
padFunctions = [
    "7",
    "8",
    "9",
    "/",
    "4",
    "5",
    "6",
    "*",
    "1",
    "2",
    "3",
    "-",
    "0",
    ".",
    "c",
    "+",
    "sin()",
    "cos()",
    "tan()",
    "^",
    "(",
    ")",
    "log()",
    "√()",
    "π",
    "e",
    "x",
    "ln()",
]

for i in range(len(padFunctions)):
    padFrame.grid_columnconfigure(i % 4, weight=1)
    padFrame.grid_rowconfigure(i // 4, weight=1)
    value = padFunctions[i]

    button = ctk.CTkButton(padFrame, text=value)
    button.grid(row=i // 4, column=i % 4, padx=5, pady=5, sticky="nsew")

    if value == "c":
        button.configure(command=lambda: inputFunction.delete(0, "end"))
    else:
        button.configure(command=lambda text=value: handleFunctionEntry(text))

# Table Frame---------------------------------------------------------------------
tableScrollableFrame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Graphic Frame-------------------------------------------------------------------
graphicFrame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)


# Command functions--------------------------------------------------------------
def handleFunctionEntry(text: str):
    inputFunction.insert("end", text)


# Fixed Point functions----------------------------------------------------------
def parseFunction(function: str):
    function = function.replace("^", "**")
    function = function.replace("π", "pi")
    function = function.replace("√", "root")
    function = function.replace("sen(", "sin(")
    function = function.replace("cos(", "cos(")
    function = function.replace("tan(", "tan(")
    function = function.replace("csc(", "csc(")
    return function

def calculateFixedPoint():
    try:
        functionValue = parseFunction(inputFunction.get())
        x0Value = float(inputX0.get())
        toleranceValue = float(inputTolerance.get())
        functionLength = len(functionValue)
        i = 0

        while i < functionLength:
            functionCopy = [*functionValue]
            if functionCopy[i] == "x":
                functionCopy[i] = "y"
                functionCopy = "".join(functionCopy)
                print(functionCopy)

            i += 1

    except Exception as e:
        print("No se pudo encontrar una solución, la función no converge " + str(e))





app.mainloop()
