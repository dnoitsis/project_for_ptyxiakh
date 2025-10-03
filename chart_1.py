import matplotlib.pyplot as plt
import numpy as np

# Set up the data from your file - thresholds in ASCENDING order
thresholds = [0.2, 0.3, 0.4, 0.5]
traffic_levels = [20, 40, 60, 80, 100, 120]

energy_data = {
    0.2: {
        'EAFFB': [3927348.0, 5774787.8, 7523717.6, 9398181.5, 11215602.8, 13223003.2],
        'Proposed': [3550196.0, 5224220.7, 6783252.8, 8420021.1, 10146792.7, 11806278.2],
        'EAFFB_Critical': [5994687.0, 8835055.9, 11469392.1, 14346214.2, 17132607.3, 20125195.0]
    },
    0.3: {
        'EAFFB': [1664458.0, 2439836.2, 3199160.0, 4003138.5, 4786366.6, 5567403.4],
        'Proposed': [1522356.0, 2230880.6, 2922350.8, 3671081.7, 4381913.1, 5102890.6],
        'EAFFB_Critical': [2174506.0, 3188448.2, 4133299.9, 5233481.5, 6235930.2, 7267199.9]
    },
    0.4: {
        'EAFFB': [1452038.0, 2140862.7, 2800650.6, 3469991.7, 4212888.8, 4922817.1],
        'Proposed': [1318712.0, 1941182.5, 2545398.8, 3164524.6, 3816407.3, 4466902.7],
        'EAFFB_Critical': [1846619.0, 2716752.7, 3560156.1, 4415787.3, 5312095.1, 6245755.1]
    },
    0.5: {
        'EAFFB': [1384970.0, 2043689.1, 2714777.8, 3344836.6, 3991000.9, 4707819.9],
        'Proposed': [1318712.0, 1945957.7, 2585386.1, 3185031.4, 3804192.4, 4495539.5],
        'EAFFB_Critical': [1465203.0, 2163216.4, 2867878.1, 3534558.2, 4221968.6, 4970921.1]
    }
}

# Create the visualization
plt.figure(figsize=(15, 10))

# Plot 1: Energy consumption comparison for threshold 0.2
plt.subplot(2, 2, 1)
x = np.arange(len(traffic_levels))
width = 0.25

plt.bar(x - width, energy_data[0.2]['EAFFB'], width, label='EAFFB', color='blue', alpha=0.7)
plt.bar(x, energy_data[0.2]['Proposed'], width, label='Proposed', color='green', alpha=0.7)
plt.bar(x + width, energy_data[0.2]['EAFFB_Critical'], width, label='EAFFB Critical', color='red', alpha=0.7)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('Threshold 0.2: Algorithm Comparison')
plt.xticks(x, traffic_levels)
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 2: Energy consumption comparison for threshold 0.5
plt.subplot(2, 2, 2)
plt.bar(x - width, energy_data[0.5]['EAFFB'], width, label='EAFFB', color='blue', alpha=0.7)
plt.bar(x, energy_data[0.5]['Proposed'], width, label='Proposed', color='green', alpha=0.7)
plt.bar(x + width, energy_data[0.5]['EAFFB_Critical'], width, label='EAFFB Critical', color='red', alpha=0.7)

plt.xlabel('Traffic Level')
plt.ylabel('Energy Consumption')
plt.title('Threshold 0.5: Algorithm Comparison')
plt.xticks(x, traffic_levels)
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 3: Performance across thresholds for traffic=100
plt.subplot(2, 2, 3)
traffic_idx = traffic_levels.index(100)

eaffb_vals = [energy_data[th]['EAFFB'][traffic_idx] for th in thresholds]
proposed_vals = [energy_data[th]['Proposed'][traffic_idx] for th in thresholds]
critical_vals = [energy_data[th]['EAFFB_Critical'][traffic_idx] for th in thresholds]

plt.plot(thresholds, eaffb_vals, 'o-', label='EAFFB', linewidth=2, markersize=8)
plt.plot(thresholds, proposed_vals, 's-', label='Proposed', linewidth=2, markersize=8)
plt.plot(thresholds, critical_vals, '^-', label='EAFFB Critical', linewidth=2, markersize=8)

plt.xlabel('Threshold Value')
plt.ylabel('Energy Consumption')
plt.title('Energy vs Threshold (Traffic = 100)')
plt.legend()
plt.grid(True, alpha=0.3)

# Plot 4: Percentage increase of EAFFB Critical vs others
plt.subplot(2, 2, 4)
improvement_data = []
for threshold in thresholds:
    avg_imp_eaffb = np.mean([(energy_data[threshold]['EAFFB_Critical'][i] - energy_data[threshold]['EAFFB'][i]) / energy_data[threshold]['EAFFB'][i] * 100
                           for i in range(len(traffic_levels))])
    avg_imp_proposed = np.mean([(energy_data[threshold]['EAFFB_Critical'][i] - energy_data[threshold]['Proposed'][i]) / energy_data[threshold]['Proposed'][i] * 100
                              for i in range(len(traffic_levels))])
    improvement_data.append([avg_imp_eaffb, avg_imp_proposed])

improvement_data = np.array(improvement_data)
x = np.arange(len(thresholds))
width = 0.35

plt.bar(x - width/2, improvement_data[:, 0], width, label='vs EAFFB', color='orange', alpha=0.7)
plt.bar(x + width/2, improvement_data[:, 1], width, label='vs Proposed', color='purple', alpha=0.7)

plt.xlabel('Threshold Value')
plt.ylabel('Energy Increase (%)')
plt.title('EAFFB Critical: Energy Increase vs Other Algorithms')
plt.xticks(x, thresholds)
plt.legend()
plt.grid(True, alpha=0.3)

# Add value labels
for i, (val1, val2) in enumerate(improvement_data):
    plt.text(i - width/2, val1 + 1, f'{val1:.1f}%', ha='center', va='bottom', fontweight='bold')
    plt.text(i + width/2, val2 + 1, f'{val2:.1f}%', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.show()