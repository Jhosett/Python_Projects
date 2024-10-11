import customtkinter as ctk
import tkinter as tk

#window ------------------------------------------------------------------------------------------
app = ctk.CTk()
app.title("Método de Punto Fijo - 192106")
app.geometry("1250x650")
#-----------------------------------------------------------------------------------------------------------

#Tittle-----------------------------------------------------------------------------------------------------
main_tittle = ctk.CTkLabel(
    app, text="Método de Punto Fijo",
)

solution_tittle = ctk.CTkLabel(
    app, text="Solución"
)

main_tittle.pack(padx=4)
solution_tittle.pack(padx=4)
#-----------------------------------------------------------------------------------------------------------

#Inputs-----------------------------------------------------------------------------------------------------
input_label = ctk.CTkLabel(
    app, text="Ingrese el valor de x0:"
)

input_label.pack(padx=4)

input_field = ctk.CTkEntry(
    app, width=200, height=30, corner_radius=10, border_width=2, border_color="#565656"
)

input_field.pack(padx=4)
#-----------------------------------------------------------------------------------------------------------

app.mainloop()