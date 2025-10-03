import matplotlib.pyplot as plt
import numpy as np

# Set up the data from your file - thresholds in ASCENDING order
thresholds = [0.2, 0.3, 0.4, 0.5]
traffic_levels = [20, 40, 60, 80, 100, 120]

energy_data = {
    0.2: {
        'EAFFB': [3927348.0, 5769491.4, 7671367.1, 9455115.1, 11320151.2, 13231476.4],
        'Proposed': [3550196.0, 5196372.1, 6882355.5, 8518912.1, 10229197.8, 11913792.6],
        'EAFFB_Critical_Fire_Flood': [11727555.0, 17181419.2, 22879637.0, 28120220.1, 33950190.5, 39412045.9],
        'Improvement_EAFFB': [-198.61, -197.80, -198.25, -197.41, -199.91, -197.87],
        'Improvement_Proposed': [-230.34, -230.64, -232.44, -230.09, -231.89, -230.81]
    },
    0.3: {
        'EAFFB': [1664458.0, 2450097.6, 3230204.3, 4013035.1, 4890363.9, 5603760.0],
        'Proposed': [1522356.0, 2244245.7, 2957417.1, 3671794.3, 4464517.4, 5127604.7],
        'EAFFB_Critical_Fire_Flood': [3614966.0, 5308652.1, 6971507.0, 8659360.8, 10569640.9, 12090263.9],
        'Improvement_EAFFB': [-117.19, -116.67, -115.82, -115.78, -116.13, -115.75],
        'Improvement_Proposed': [-137.46, -136.55, -135.73, -135.83, -136.75, -135.79]
    },
    0.4: {
        'EAFFB': [1452038.0, 2138754.6, 2818739.8, 3463296.8, 4160750.6, 4863825.0],
        'Proposed': [1318712.0, 1941956.2, 2564936.2, 3148546.4, 3791164.4, 4440159.2],
        'EAFFB_Critical_Fire_Flood': [3128132.0, 4567460.3, 6039067.9, 7393961.3, 8908113.9, 10435939.8],
        'Improvement_EAFFB': [-115.43, -113.56, -114.25, -113.49, -114.10, -114.56],
        'Improvement_Proposed': [-137.21, -135.20, -135.45, -134.84, -134.97, -135.04]
    },
    0.5: {
        'EAFFB': [1384970.0, 2040442.4, 2692669.5, 3349189.9, 4031905.1, 4710395.2],
        'Proposed': [1318712.0, 1944715.4, 2566152.3, 3192367.2, 3837392.8, 4485644.6],
        'EAFFB_Critical_Fire_Flood': [2436916.0, 3592323.9, 4716823.1, 5861408.6, 7013614.9, 8226657.3],
        'Improvement_EAFFB': [-75.95, -76.06, -75.17, -75.01, -73.95, -74.65],
        'Improvement_Proposed': [-84.80, -84.72, -83.81, -83.61, -82.77, -83.40]
    }
}

# Create the visualization
plt.figure(figsize=(16, 12))

# Plot 1: Energy consumption comparison for threshold 0.2 (most critical)
plt.subplot(2, 3, 1)
x = np.arange(len(traffic_levels))
width = 0.25

plt.bar(x - width, energy_data[0.2]['EAFFB'], width, label='EAFFB', color='blue', alpha=0.7)
plt.bar(x, energy_data[0.2]['Proposed'], width, label='Proposed', color='green', alpha=0.7)
plt.bar(x + width, energy_data[0.2]['EAFFB_Critical_Fire_Flood'], width,
        label='EAFFB Critical + Fire/Flood', color='red', alpha=0.7)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('Threshold 0.2: Algorithm Comparison\n(Most Critical Regions)')
plt.xticks(x, traffic_levels)
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)

# Plot 2: Energy consumption comparison for threshold 0.5 (least critical)
plt.subplot(2, 3, 2)
plt.bar(x - width, energy_data[0.5]['EAFFB'], width, label='EAFFB', color='blue', alpha=0.7)
plt.bar(x, energy_data[0.5]['Proposed'], width, label='Proposed', color='green', alpha=0.7)
plt.bar(x + width, energy_data[0.5]['EAFFB_Critical_Fire_Flood'], width,
        label='EAFFB Critical + Fire/Flood', color='red', alpha=0.7)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('Threshold 0.5: Algorithm Comparison\n(Least Critical Regions)')
plt.xticks(x, traffic_levels)
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)

# Plot 3: Performance across thresholds for traffic=100
plt.subplot(2, 3, 3)
traffic_idx = traffic_levels.index(100)

eaffb_vals = [energy_data[th]['EAFFB'][traffic_idx] for th in thresholds]
proposed_vals = [energy_data[th]['Proposed'][traffic_idx] for th in thresholds]
critical_vals = [energy_data[th]['EAFFB_Critical_Fire_Flood'][traffic_idx] for th in thresholds]

plt.plot(thresholds, eaffb_vals, 'o-', label='EAFFB', linewidth=2, markersize=8)
plt.plot(thresholds, proposed_vals, 's-', label='Proposed', linewidth=2, markersize=8)
plt.plot(thresholds, critical_vals, '^-', label='EAFFB Critical + Fire/Flood', linewidth=2, markersize=8)

plt.xlabel('Threshold Value')
plt.ylabel('Energy Consumption')
plt.title('Energy vs Threshold (Traffic = 100)')
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)

# Plot 4: Percentage increase of EAFFB Critical + Fire/Flood vs others
plt.subplot(2, 3, 4)
improvement_data = []
for threshold in thresholds:
    avg_imp_eaffb = np.mean(energy_data[threshold]['Improvement_EAFFB'])
    avg_imp_proposed = np.mean(energy_data[threshold]['Improvement_Proposed'])
    improvement_data.append([avg_imp_eaffb, avg_imp_proposed])

improvement_data = np.array(improvement_data)
x = np.arange(len(thresholds))
width = 0.35

bars1 = plt.bar(x - width/2, improvement_data[:, 0], width, label='vs EAFFB', color='orange', alpha=0.7)
bars2 = plt.bar(x + width/2, improvement_data[:, 1], width, label='vs Proposed', color='purple', alpha=0.7)

plt.xlabel('Threshold Value')
plt.ylabel('Energy Increase (%)')
plt.title('EAFFB Critical + Fire/Flood:\nEnergy Increase vs Other Algorithms')
plt.xticks(x, thresholds)
plt.legend()
plt.grid(True, alpha=0.3)

# Add value labels
for i, (val1, val2) in enumerate(improvement_data):
    plt.text(i - width/2, val1 + 5, f'{val1:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
    plt.text(i + width/2, val2 + 5, f'{val2:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)

# Plot 5: Energy consumption growth with traffic for EAFFB Critical + Fire/Flood
plt.subplot(2, 3, 5)
for threshold in thresholds:
    plt.plot(traffic_levels, energy_data[threshold]['EAFFB_Critical_Fire_Flood'],
             'o-', label=f'Threshold {threshold}', linewidth=2, markersize=6)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('EAFFB Critical + Fire/Flood:\nEnergy vs Traffic by Threshold')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 6: Comparison of all algorithms at threshold 0.3
plt.subplot(2, 3, 6)
threshold = 0.3
data = energy_data[threshold]
x = np.arange(len(traffic_levels))
width = 0.25

plt.bar(x - width, data['EAFFB'], width, label='EAFFB', color='blue', alpha=0.7)
plt.bar(x, data['Proposed'], width, label='Proposed', color='green', alpha=0.7)
plt.bar(x + width, data['EAFFB_Critical_Fire_Flood'], width,
        label='EAFFB Critical + Fire/Flood', color='red', alpha=0.7)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('Threshold 0.3: Algorithm Comparison')
plt.xticks(x, traffic_levels)
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print key insights
print("="*70)
print("KEY INSIGHTS: EAFFB with Critical Nodes + Fire/Flood Disasters Logic")
print("="*70)
print("🚨 CRITICAL OBSERVATIONS:")
print(f"• EAFFB with Fire/Flood logic uses SIGNIFICANTLY MORE energy than both algorithms")
print(f"• At threshold 0.2: Uses 200-230% MORE energy than other algorithms")
print(f"• At threshold 0.5: Uses 75-85% MORE energy than other algorithms")
print(f"• Performance gap INCREASES dramatically with more critical regions (lower thresholds)")
print(f"• Fire/Flood disaster logic adds SUBSTANTIAL energy overhead")
print(f"• Proposed algorithm remains MOST EFFICIENT across all scenarios")
print("="*70)