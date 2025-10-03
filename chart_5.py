import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import StringIO


# First, let's parse the data and structure it for analysis
def parse_experiment_data(text_data):
    # This function would parse the text data into a structured format
    # For now, I'll create a sample dataset based on the patterns observed
    algorithms = ['EAFFB', 'EAFFB2', 'Proposed', 'EAFFB_new_shortest', 'EAFFB_critical', 'EAFFB_disaster']

    data = []
    thresholds = [0.5, 0.4, 0.3, 0.2]
    traffic_levels = [20, 40, 60, 80, 100, 120]

    # Sample data structure (you would replace this with actual parsed data)
    for threshold in thresholds:
        for traffic in traffic_levels:
            for algo in algorithms:
                # This is simplified - you'd extract actual values from your data
                energy = np.random.uniform(1000000, 5000000)
                laying_cost = np.random.uniform(0, 10000000000)
                repair_cost = np.random.uniform(1000000, 5000000)
                repair_hours = np.random.uniform(300, 2000)

                data.append({
                    'threshold': threshold,
                    'traffic': traffic,
                    'algorithm': algo,
                    'energy': energy,
                    'laying_cost': laying_cost,
                    'repair_cost': repair_cost,
                    'repair_hours': repair_hours
                })

    return pd.DataFrame(data)


# Create the visualization charts
def create_comprehensive_charts(df):
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Algorithm Performance Analysis Across Different Thresholds and Traffic Levels',
                 fontsize=16, fontweight='bold')

    # Chart 1: Energy Consumption vs Traffic for different algorithms (threshold=0.5)
    threshold_05 = df[df['threshold'] == 0.5]
    for algo in threshold_05['algorithm'].unique():
        algo_data = threshold_05[threshold_05['algorithm'] == algo]
        axes[0, 0].plot(algo_data['traffic'], algo_data['energy'], marker='o', label=algo, linewidth=2)

    axes[0, 0].set_title('Energy vs Traffic (Threshold=0.5)')
    axes[0, 0].set_xlabel('Average Traffic')
    axes[0, 0].set_ylabel('Energy Consumption')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    # Chart 2: Energy Comparison across thresholds for EAFFB2
    eaffb2_data = df[df['algorithm'] == 'EAFFB2']
    for threshold in eaffb2_data['threshold'].unique():
        threshold_data = eaffb2_data[eaffb2_data['threshold'] == threshold]
        axes[0, 1].plot(threshold_data['traffic'], threshold_data['energy'],
                        marker='s', label=f'Thresh={threshold}', linewidth=2)

    axes[0, 1].set_title('EAFFB2: Energy vs Traffic for Different Thresholds')
    axes[0, 1].set_xlabel('Average Traffic')
    axes[0, 1].set_ylabel('Energy Consumption')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)

    # Chart 3: Cost Analysis (Laying + Repair) for threshold=0.2
    threshold_02 = df[df['threshold'] == 0.2]
    algorithms = threshold_02['algorithm'].unique()
    laying_costs = [threshold_02[threshold_02['algorithm'] == algo]['laying_cost'].mean() for algo in algorithms]
    repair_costs = [threshold_02[threshold_02['algorithm'] == algo]['repair_cost'].mean() for algo in algorithms]

    x = np.arange(len(algorithms))
    width = 0.35

    axes[0, 2].bar(x - width / 2, laying_costs, width, label='Laying Cost', alpha=0.8)
    axes[0, 2].bar(x + width / 2, repair_costs, width, label='Repair Cost', alpha=0.8)
    axes[0, 2].set_title('Cost Analysis (Threshold=0.2)')
    axes[0, 2].set_xlabel('Algorithms')
    axes[0, 2].set_ylabel('Cost ($)')
    axes[0, 2].set_xticks(x)
    axes[0, 2].set_xticklabels(algorithms, rotation=45)
    axes[0, 2].legend()
    axes[0, 2].grid(True, alpha=0.3)

    # Chart 4: Repair Hours vs Threshold
    repair_hours_data = df.groupby(['algorithm', 'threshold'])['repair_hours'].mean().unstack()
    repair_hours_data.plot(kind='bar', ax=axes[1, 0], width=0.8)
    axes[1, 0].set_title('Average Repair Hours vs Algorithm and Threshold')
    axes[1, 0].set_xlabel('Algorithm')
    axes[1, 0].set_ylabel('Repair Hours')
    axes[1, 0].tick_params(axis='x', rotation=45)
    axes[1, 0].grid(True, alpha=0.3)

    # Chart 5: Performance Improvement (%) - EAFFB2 vs EAFFB
    eaffb_energy = df[df['algorithm'] == 'EAFFB'].groupby('traffic')['energy'].mean()
    eaffb2_energy = df[df['algorithm'] == 'EAFFB2'].groupby('traffic')['energy'].mean()
    improvement = ((eaffb_energy - eaffb2_energy) / eaffb_energy) * 100

    axes[1, 1].bar(improvement.index, improvement.values, color='green', alpha=0.7)
    axes[1, 1].set_title('EAFFB2 vs EAFFB: Energy Improvement (%)')
    axes[1, 1].set_xlabel('Average Traffic')
    axes[1, 1].set_ylabel('Improvement (%)')
    axes[1, 1].grid(True, alpha=0.3)

    # Chart 6: 3D-like visualization using heatmap for energy consumption
    pivot_data = df[df['algorithm'] == 'Proposed'].pivot_table(
        values='energy', index='traffic', columns='threshold'
    )
    im = axes[1, 2].imshow(pivot_data.values, cmap='viridis', aspect='auto')
    axes[1, 2].set_title('Proposed Algorithm: Energy Heatmap')
    axes[1, 2].set_xlabel('Threshold')
    axes[1, 2].set_ylabel('Traffic')
    axes[1, 2].set_xticks(range(len(pivot_data.columns)))
    axes[1, 2].set_xticklabels(pivot_data.columns)
    axes[1, 2].set_yticks(range(len(pivot_data.index)))
    axes[1, 2].set_yticklabels(pivot_data.index)
    plt.colorbar(im, ax=axes[1, 2], label='Energy Consumption')

    plt.tight_layout()
    plt.show()


# Additional specialized charts
def create_specialized_charts(df):
    # Chart 7: Trade-off analysis between energy and cost
    fig, ax = plt.subplots(1, 2, figsize=(15, 6))

    # Energy vs Laying Cost scatter plot
    colors = plt.cm.Set1(np.linspace(0, 1, len(df['algorithm'].unique())))
    for i, algo in enumerate(df['algorithm'].unique()):
        algo_data = df[df['algorithm'] == algo]
        ax[0].scatter(algo_data['energy'], algo_data['laying_cost'],
                      c=[colors[i]], label=algo, alpha=0.7, s=60)

    ax[0].set_xlabel('Energy Consumption')
    ax[0].set_ylabel('Laying Cost')
    ax[0].set_title('Energy vs Laying Cost Trade-off')
    ax[0].legend()
    ax[0].grid(True, alpha=0.3)

    # Algorithm comparison at fixed traffic (80)
    traffic_80 = df[df['traffic'] == 80]
    algorithms = traffic_80['algorithm'].unique()
    energy_values = [traffic_80[traffic_80['algorithm'] == algo]['energy'].mean() for algo in algorithms]

    bars = ax[1].bar(algorithms, energy_values, color=colors[:len(algorithms)])
    ax[1].set_xlabel('Algorithms')
    ax[1].set_ylabel('Average Energy Consumption')
    ax[1].set_title('Algorithm Comparison at Traffic=80')
    ax[1].tick_params(axis='x', rotation=45)
    ax[1].grid(True, alpha=0.3)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax[1].text(bar.get_x() + bar.get_width() / 2., height,
                   f'{height / 1000000:.1f}M',
                   ha='center', va='bottom')

    plt.tight_layout()
    plt.show()


# Create trend analysis chart
def create_trend_analysis(df):
    fig, ax = plt.subplots(figsize=(12, 8))

    # Analyze how each algorithm scales with traffic
    for algo in ['EAFFB', 'EAFFB2', 'Proposed', 'EAFFB_critical']:
        algo_data = df[df['algorithm'] == algo]
        avg_energy = algo_data.groupby('traffic')['energy'].mean()

        ax.plot(avg_energy.index, avg_energy.values, marker='o', linewidth=3,
                label=algo, markersize=8)

    ax.set_xlabel('Average Traffic', fontsize=12)
    ax.set_ylabel('Energy Consumption', fontsize=12)
    ax.set_title('Algorithm Scalability: Energy Consumption vs Traffic Load', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')

    plt.tight_layout()
    plt.show()


# Main execution
if __name__ == "__main__":
    # Parse your actual data here
    # df = parse_experiment_data(your_actual_data)

    # For demonstration, create sample data
    np.random.seed(42)  # For reproducible results
    df = parse_experiment_data("")

    # Create all charts
    create_comprehensive_charts(df)
    create_specialized_charts(df)
    create_trend_analysis(df)