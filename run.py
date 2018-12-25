from model import BikeShare
import matplotlib.pyplot as plt
import numpy as np
# from mesa.batchrunner import BatchRunner

number_of_days = 1
hours_in_day = 24

model = BikeShare(100, 10, 10, 10)
for i in range(number_of_days * hours_in_day):
    model.step()

# plot the end results
rider_counts = np.zeros((model.grid.width, model.grid.height))
for cell in model.grid.coord_iter():
    cell_content, x, y = cell
    rider_count = len(cell_content)
    rider_counts[x][y] = rider_count

plt.imshow(rider_counts, interpolation="nearest")
plt.colorbar()

plt.show()

# value of the grid
# param_values = {"width":  10,
#                 "height": 10,
#                 "N": range(10, 500, 10)}

# batch_run = BatchRunner(MoneyModel,
#                         parameter_values=param_values,
#                         iterations=5,
#                         max_steps=100,
#                         model_reporters={"Gini": compute_gini})

# batch_run.run_all()

# run_data = batch_run.get_model_vars_dataframe()
# run_data.head()
# plt.scatter(run_data.N, run_data.Gini)
