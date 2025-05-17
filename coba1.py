import streamlit as st
import numpy as np
from sympy import symbols, sympify, diff, lambdify
import plotly.graph_objs as go

st.title("Aplikasi Turunan Parsial dan Bidang Singgung")
st.write("Masukkan fungsi dua variabel \( f(x, y) \) dan titik evaluasi \( (x_0, y_0) \) untuk menghitung turunan parsial serta menampilkan grafik permukaan dan bidang singgung.")

# Input from user
func_input = st.text_input("Fungsi f(x, y):", "x**2 + 3*x*y + y**2")
x0 = st.number_input("x₀:", value=1.0)
y0 = st.number_input("y₀:", value=2.0)

try:
    x, y = symbols('x y')
    f_expr = sympify(func_input)
    df_dx = diff(f_expr, x)
    df_dy = diff(f_expr, y)

    f_func = lambdify((x, y), f_expr, 'numpy')
    df_dx_func = lambdify((x, y), df_dx, 'numpy')
    df_dy_func = lambdify((x, y), df_dy, 'numpy')

    z0 = f_func(x0, y0)
    df_dx_val = df_dx_func(x0, y0)
    df_dy_val = df_dy_func(x0, y0)

    st.latex(f"\frac{{\partial f}}{{\partial x}} = {str(df_dx)}")
    st.latex(f"\frac{{\partial f}}{{\partial y}} = {str(df_dy)}")
    st.write(f"Nilai turunan parsial di titik ({x0}, {y0}):")
    st.write(f"∂f/∂x = {df_dx_val}")
    st.write(f"∂f/∂y = {df_dy_val}")

    # Plot
    X_vals = np.linspace(x0 - 2, x0 + 2, 50)
    Y_vals = np.linspace(y0 - 2, y0 + 2, 50)
    X, Y = np.meshgrid(X_vals, Y_vals)
    Z = f_func(X, Y)
    Z_tangent = z0 + df_dx_val * (X - x0) + df_dy_val * (Y - y0)

    surface = go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', name='f(x, y)')
    tangent_plane = go.Surface(x=X, y=Y, z=Z_tangent, colorscale='Reds', opacity=0.5, name='Tangent Plane')
    point = go.Scatter3d(x=[x0], y=[y0], z=[z0], mode='markers', marker=dict(size=5, color='black'), name='Evaluation Point')

    fig = go.Figure(data=[surface, tangent_plane, point])
    fig.update_layout(title='Grafik f(x, y) dan Bidang Singgung',
                      scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'))

    st.plotly_chart(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")