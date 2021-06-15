import os

import matplotlib.pyplot as plt
import pandas as pd

# get ground truth
ground_truth = pd.read_csv("../../data/ercot_hourly_load.csv").iloc[-1000:]
ground_truth["Hour_Ending"] = pd.to_datetime(ground_truth["Hour_Ending"])
ground_truth = ground_truth.set_index("Hour_Ending")
ground_truth = ground_truth[
    (ground_truth.index > "2021-06-13 00:00:00")
    & (ground_truth.index <= "2021-06-20 00:00:00")
]

# load submissions and calculate RMSE
submission_dir = "./submissions"
submissions = dict()
rmse = []
team_dirs = sorted(os.listdir(submission_dir))
for team_dir in team_dirs:
    team_name = team_dir[5:]
    submission_csvs = sorted(os.listdir(os.path.join(submission_dir, team_dir)))
    submission_csv = submission_csvs[-1]
    df = pd.read_csv(os.path.join(submission_dir, team_dir, submission_csv))
    df["Hour_Ending"] = pd.to_datetime(df["Hour_Ending"])
    df = df.set_index("Hour_Ending")
    submissions[team_name] = df

    rmse.append(
        {
            "Team": team_name,
            "RMSE": (
                ((ground_truth - df) ** 2).sum().sum()
                / (ground_truth.shape[0] * ground_truth.shape[1])
            )
            ** 0.5,
        }
    )
rmse = pd.DataFrame(rmse).sort_values("RMSE")
rmse = rmse.set_index("Team")
rmse = rmse.reset_index()

# write leaderboard
rmse.to_markdown("../../leaderboard/README.md")
leaderboard_time = ground_truth.index[-1]
if leaderboard_time >= pd.to_datetime("2021-06-20 00:00:00-05:00"):
    is_final = ""
else:
    is_final = "NOT "
with open("../../leaderboard/README.md", "a") as f:
    f.write("\n\n")
    f.write(
        f"Leaderboard up to {leaderboard_time}. This is {is_final}the final ranking."
    )

# plot comparison charts
f, axes = plt.subplots(
    nrows=ground_truth.shape[1], figsize=(10, 5 * ground_truth.shape[1]), sharex=True
)
for zone, ax in zip(ground_truth.columns, axes):
    zone_pred = pd.concat(
        [
            submission[zone].rename(team_name)
            for team_name, submission in submissions.items()
        ],
        axis=1,
    )
    ground_truth[zone].rename("Ground Truth").plot(ax=ax, linewidth=5)
    zone_pred.plot(ax=ax, legend=None, linewidth=0.5)
    ax.set_title(zone)
    if ax is axes[0]:
        ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.02))

plt.savefig("../../leaderboard/comparison.png", bbox_inches="tight")
