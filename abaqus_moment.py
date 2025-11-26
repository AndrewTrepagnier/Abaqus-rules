import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


def draw_nozzle(ax, direction, length=0.8, radius=0.15):
    
    sign = 1 if direction[0] == '+' else -1
    axis = direction[1].lower()
    
    n_segments = 20
    theta = np.linspace(0, 2*np.pi, n_segments)
    
    if axis == 'x':
        x = np.linspace(0, sign*length, 2)
        y = radius * np.cos(theta)
        z = radius * np.sin(theta)
        X, Y = np.meshgrid(x, y)
        X, Z = np.meshgrid(x, z)
    elif axis == 'y':
        y = np.linspace(0, sign*length, 2)
        x = radius * np.cos(theta)
        z = radius * np.sin(theta)
        Y, X = np.meshgrid(y, x)
        Y, Z = np.meshgrid(y, z)
    else:  # z
        z = np.linspace(0, sign*length, 2)
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
        Z, X = np.meshgrid(z, x)
        Z, Y = np.meshgrid(z, y)
    
    ax.plot_surface(X, Y, Z, alpha=0.3, color='gray', edgecolor='darkgray', linewidth=0.5)
    
    
    if axis == 'x':
        x_cap = np.full_like(theta, sign*length)
        y_cap = radius * np.cos(theta)
        z_cap = radius * np.sin(theta)
    elif axis == 'y':
        y_cap = np.full_like(theta, sign*length)
        x_cap = radius * np.cos(theta)
        z_cap = radius * np.sin(theta)
    else:
        z_cap = np.full_like(theta, sign*length)
        x_cap = radius * np.cos(theta)
        y_cap = radius * np.sin(theta)
    
    verts = [list(zip(x_cap, y_cap, z_cap))]
    ax.add_collection3d(Poly3DCollection(verts, alpha=0.4, facecolor='lightblue', edgecolor='darkblue'))


def plot_nozzle_moments(RF, RM, nozzle_direction):
    """Visualize forces and moments at nozzle tip."""
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')
    
    
    draw_nozzle(ax, nozzle_direction)
    
    
    sign = 1 if nozzle_direction[0] == '+' else -1
    axis = nozzle_direction[1].lower()
    nozzle_length = 0.8
    
    tip = np.array([0., 0., 0.])
    if axis == 'x':
        tip[0] = sign * nozzle_length
    elif axis == 'y':
        tip[1] = sign * nozzle_length
    else:  # z
        tip[2] = sign * nozzle_length
    
    
    axis_len = 0.35
    ax.quiver(tip[0], tip[1], tip[2], axis_len, 0, 0, 
              color ='red', linewidth=2, alpha=0.7, arrow_length_ratio=0.15)
    ax.text(tip[0]+axis_len* 1.15, tip[1], tip[2] , "X", 
            color='red', fontsize=11, fontweight='bold')
    
    ax.quiver(tip[0], tip[1], tip[2], 0, axis_len, 0,
              color='green', linewidth=2, alpha=0.7, arrow_length_ratio=0.15)
    ax.text(tip[0], tip[1]+axis_len*1.15, tip[2], "Y",
            color='green', fontsize=11, fontweight='bold')
    
    ax.quiver(tip[0], tip[1], tip[2], 0, 0, axis_len,
              color='blue' , linewidth=2, alpha=0.7, arrow_length_ratio=0.15)
    ax.text(tip[0], tip[1], tip[2]+axis_len*1.15, "Z",
            color='blue', fontsize=11, fontweight='bold')
    
    
    ax.scatter([tip[0]], [tip[1]], [tip[2]], 
               color='red', s=100, marker='o', edgecolors='black', linewidths=1.5, zorder=10)
    
     
    RF_mag = np.linalg.norm(RF)

    if RF_mag>1e-6:

        RF_scaled = RF / RF_mag* 0.45

        ax.quiver(tip[0], tip[1], tip[2], 

                  RF_scaled[0], RF_scaled[1], RF_scaled[2],
                  color='orange', linewidth=4, arrow_length_ratio=0.15, alpha=0.9)
    
  
    RM_mag = np.linalg.norm(RM)
    if RM_mag > 1e-6:
        n = RM / RM_mag
        
        arbitrary = np.array([1.0, 0.0, 0.0])
        if abs(np.dot(arbitrary, n)) > 0.9:
            arbitrary = np.array([0.0, 1.0, 0.0])
        
        v1 = np.cross(n, arbitrary)
        v1 = v1 / np.linalg.norm(v1)
        v2 = np.cross(n, v1)
   
        r = 0.32
        theta = np.linspace(0, 1.85*np.pi, 200)
        circle = np.outer(np.cos(theta), v1) * r + np.outer(np.sin(theta), v2) * r
        circle[:, 0] += tip[0]
        circle[:, 1] += tip[1]
        circle[:, 2] += tip[2]
        
        ax.plot(circle[:, 0], circle[:, 1], circle[:, 2],
                color='purple', linewidth=3.5, alpha=0.9)
        
     
        for arrow_idx in [150, 180]:
            arrow_angle = theta[arrow_idx]
            arrow_point = tip + (np.cos(arrow_angle)*v1 + np.sin(arrow_angle)*v2) * r
            arrow_dir = (-np.sin(arrow_angle)*v1 + np.cos(arrow_angle)*v2) * 0.12
            
            ax.quiver(arrow_point[0], arrow_point[1], arrow_point[2],
                      arrow_dir[0], arrow_dir[1], arrow_dir[2],
                      color='purple', linewidth=2.5, arrow_length_ratio=0.5, alpha=0.9)
        
       
        axis_scale = 0.45
        ax.plot([tip[0], tip[0]+n[0]*axis_scale], 
                [tip[1], tip[1]+n[1]*axis_scale], 
                [tip[2], tip[2]+n[2]*axis_scale],
                'purple', linestyle='--', linewidth=2.5, alpha=0.7)
    
 
    max_range = 1.1
    ax.set_xlim([-max_range, max_range])
    ax.set_ylim([-max_range, max_range])
    ax.set_zlim([-max_range, max_range])
    
    ax.set_xlabel("X", fontsize=10, fontweight='bold')
    ax.set_ylabel("Y", fontsize=10, fontweight='bold')
    ax.set_zlabel("Z", fontsize=10, fontweight='bold')
    
    ax.view_init(elev=20, azim=45)
    ax.grid(True, alpha=0.2)
    
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    
    print("\nNOZZLE MOMENT CHECKER")
    print("="*50)
    
    
    nozzle_dir = input("Nozzle direction (+x,-x,+y,-y,+z,-z): ").strip().lower()
    
    
    print("\nReaction Forces:")
    rfx = float(input("  RFx = "))
    rfy = float(input("  RFy = "))
    rfz = float(input("  RFz = "))
    RF = np.array([rfx, rfy, rfz])
    
  
    print("\nReaction Moments:")
    rmx = float(input("  RMx = "))
    rmy = float(input("  RMy = "))
    rmz = float(input("  RMz = "))
    RM = np.array([rmx, rmy, rmz])
    
    print("\n" + "="*50)
    print(f"RF: [{RF[0]:.2e}, {RF[1]:.2e}, {RF[2]:.2e}]")
    print(f"RM: [{RM[0]:.2e}, {RM[1]:.2e}, {RM[2]:.2e}]")
    print("="*50 + "\n")
    
    plot_nozzle_moments(RF, RM, nozzle_dir)
