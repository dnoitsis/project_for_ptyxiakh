import matplotlib.pyplot as plt
import numpy as np

# Set up the data from your file - thresholds in ASCENDING order
thresholds = [0.2, 0.3, 0.4, 0.5]
traffic_levels = [20, 40, 60, 80, 100, 120]

energy_data = {
    0.2: {
        'EAFFB': [3927348.0, 5764094.1, 7655220.9, 9432180.4, 11384032.5, 13137357.7],
        'Proposed': [3550196.0, 5206842.1, 6848905.1, 8464586.7, 10216184.1, 11820517.8],
        'EAFFB2': [3293151.0, 4833022.0, 6395624.9, 7896949.1, 9520476.0, 11018443.6],
        'Improvement_EAFFB': [16.15, 16.15, 16.45, 16.28, 16.37, 16.13],
        'Improvement_Proposed': [7.24, 7.18, 6.62, 6.71, 6.81, 6.79]
    },
    0.3: {
        'EAFFB': [1664458.0, 2426913.3, 3196168.8, 4024378.6, 4790279.1, 5590225.5],
        'Proposed': [1522356.0, 2217150.4, 2927968.5, 3673035.4, 4382415.3, 5113010.3],
        'EAFFB2': [1511452.0, 2200954.4, 2909667.4, 3650861.3, 4349143.3, 5084922.3],
        'Improvement_EAFFB': [9.19, 9.31, 8.96, 9.28, 9.21, 9.04],
        'Improvement_Proposed': [0.72, 0.73, 0.63, 0.60, 0.76, 0.55]
    },
    0.4: {
        'EAFFB': [1452038.0, 2145671.5, 2842417.5, 3523544.1, 4220961.6, 4920793.8],
        'Proposed': [1318712.0, 1947664.3, 2572969.9, 3191869.4, 3833360.6, 4474467.8],
        'EAFFB2': [1318712.0, 1947664.3, 2572969.9, 3191869.4, 3833360.6, 4474467.8],
        'Improvement_EAFFB': [9.18, 9.23, 9.48, 9.41, 9.18, 9.07],
        'Improvement_Proposed': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    0.5: {
        'EAFFB': [1384970.0, 2038884.7, 2702009.8, 3367556.6, 3984577.5, 4731068.7],
        'Proposed': [1318712.0, 1942400.0, 2575007.9, 3204149.9, 3799551.5, 4511288.9],
        'EAFFB2': [1318712.0, 1942400.0, 2575007.9, 3204149.9, 3799551.5, 4511288.9],
        'Improvement_EAFFB': [4.78, 4.73, 4.70, 4.85, 4.64, 4.65],
        'Improvement_Proposed': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
}

# Create the visualization
plt.figure(figsize=(18, 12))

# Plot 1: Energy consumption comparison for threshold 0.2 (most critical)
plt.subplot(2, 3, 1)
x = np.arange(len(traffic_levels))
width = 0.25

plt.bar(x - width, energy_data[0.2]['EAFFB'], width, label='EAFFB', color='blue', alpha=0.7)
plt.bar(x, energy_data[0.2]['Proposed'], width, label='Proposed', color='green', alpha=0.7)
plt.bar(x + width, energy_data[0.2]['EAFFB2'], width,
        label='EAFFB2 (New Shortest Path)', color='red', alpha=0.7)

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
plt.bar(x + width, energy_data[0.5]['EAFFB2'], width,
        label='EAFFB2 (New Shortest Path)', color='red', alpha=0.7)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('Threshold 0.5: Algorithm Comparison\n(Least Critical Regions)')
plt.xticks(x, traffic_levels)
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)

# Plot 3: Performance improvement of EAFFB2 vs other algorithms
plt.subplot(2, 3, 3)
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
plt.ylabel('Energy Reduction (%)')
plt.title('EAFFB2: Energy Reduction vs Other Algorithms')
plt.xticks(x, thresholds)
plt.legend()
plt.grid(True, alpha=0.3)

# Add value labels
for i, (val1, val2) in enumerate(improvement_data):
    plt.text(i - width/2, val1 + 0.5, f'{val1:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
    plt.text(i + width/2, val2 + 0.5, f'{val2:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)

# Plot 4: Energy consumption trends across thresholds for traffic=100
plt.subplot(2, 3, 4)
traffic_idx = traffic_levels.index(100)

eaffb_vals = [energy_data[th]['EAFFB'][traffic_idx] for th in thresholds]
proposed_vals = [energy_data[th]['Proposed'][traffic_idx] for th in thresholds]
eaffb2_vals = [energy_data[th]['EAFFB2'][traffic_idx] for th in thresholds]

plt.plot(thresholds, eaffb_vals, 'o-', label='EAFFB', linewidth=2, markersize=8)
plt.plot(thresholds, proposed_vals, 's-', label='Proposed', linewidth=2, markersize=8)
plt.plot(thresholds, eaffb2_vals, '^-', label='EAFFB2', linewidth=2, markersize=8)

plt.xlabel('Threshold Value')
plt.ylabel('Energy Consumption')
plt.title('Energy vs Threshold (Traffic = 100)')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 5: EAFFB2 performance across all traffic levels
plt.subplot(2, 3, 5)
for threshold in thresholds:
    plt.plot(traffic_levels, energy_data[threshold]['EAFFB2'],
             'o-', label=f'Threshold {threshold}', linewidth=2, markersize=6)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('EAFFB2: Energy vs Traffic by Threshold')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 6: Direct comparison at threshold 0.3 showing EAFFB2 superiority
plt.subplot(2, 3, 6)
threshold = 0.3
data = energy_data[threshold]
x = np.arange(len(traffic_levels))
width = 0.25

plt.bar(x - width, data['EAFFB'], width, label='EAFFB', color='blue', alpha=0.7)
plt.bar(x, data['Proposed'], width, label='Proposed', color='green', alpha=0.7)
plt.bar(x + width, data['EAFFB2'], width,
        label='EAFFB2 (New Shortest Path)', color='red', alpha=0.7)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('Threshold 0.3: EAFFB2 Outperforms Both')
plt.xticks(x, traffic_levels)
plt.legend(fontsize=8)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Print key insights
print("="*70)
print("KEY INSIGHTS: EAFFB2 with New Shortest Path Calculation Scheme")
print("="*70)
print("✅ POSITIVE RESULTS:")
print(f"• EAFFB2 consistently REDUCES energy consumption vs original EAFFB")
print(f"• At threshold 0.2: 16.1-16.5% energy reduction vs EAFFB")
print(f"• At threshold 0.2: 6.6-7.2% energy reduction vs Proposed Algorithm")
print(f"• At threshold 0.3: EAFFB2 outperforms BOTH algorithms")
print(f"• New shortest path scheme provides SIGNIFICANT improvements")
print(f"• Performance benefits INCREASE with more critical regions (lower thresholds)")
print("")
print("📊 PERFORMANCE SUMMARY:")
print(f"• Threshold 0.2: EAFFB2 > Proposed > EAFFB")
print(f"• Threshold 0.3: EAFFB2 > Proposed > EAFFB")
print(f"• Threshold 0.4-0.5: EAFFB2 = Proposed > EAFFB")
print("="*70)