import datetime
import os
from math import cos

import pandas as pd

headers_trajectory = ['latitude', 'longitude', 'timestamp', 'date', 'time', 'name']


def load_trajectory_df(full_filename):
    df = pd.read_csv(full_filename, names=headers_trajectory)

    for itm in range(len(df)):
        value = int(df['timestamp'][itm])
        date = datetime.datetime.fromtimestamp(value).strftime('%d/%m/%Y')
        time = datetime.datetime.fromtimestamp(value).strftime('%H:%M:%S')
        timestamp = datetime.datetime.fromtimestamp(value).strftime('%d/%m/%Y %H:%M:%S')

        df['date'][itm] = date
        df['time'][itm] = time
        df['timestamp'][itm] = timestamp

        # Calculating the Latitude and Longitude
        lat = 46
        lon = 11

        a = df['longitude'][itm] / 6076 / 60
        b = df['latitude'][itm] / 4145 / 60
        c = lon + b
        latitude = lat + a
        latitude = round(latitude, 5)
        longitude = c - (df['latitude'][itm] / (6076 * cos(itm)) / 60)
        longitude = round(longitude, 5)

        df['latitude'][itm] = latitude
        df['longitude'][itm] = longitude

    df.drop(['timestamp'], axis=1, inplace=True)

    return df


OUTPUT_FOLDER = 'processed_data/'

if __name__ == '__main__':

    # dir_target = input("Please, give a path to data: ").strip()
    dir_target = "/Users/admin/Documents/Data Trajectory/"
    os.chdir(dir_target)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    list_df_traj = []

    for file in os.listdir(os.path.curdir):
        conversion = load_trajectory_df(file)

        list_df_traj = [conversion]

        # print(len(list_df_traj))

        # sys.exit(0)

        print(os.path.basename(file))

        # for df in list_df_traj:
        #     print(df)
        cols = ""
        for df in list_df_traj:
            for i in range(len(list_df_traj)):
                df['name'] = os.path.basename(file)
                cols = df.columns.tolist()
                cols = cols[-1:] + cols[:-1]
                df = df.ix[:, cols]
        print(list_df_traj)

        # sys.exit(1)
        df_traj_all = pd.concat(list_df_traj)

        # output_filename = os.path.basename(file) + ".modified"
        output_filename = os.path.basename(file)
        # if True:
        #     print(df_traj_all)
        #     sys.exit(0)
        # continue
        print("Saving as: {}".format(os.path.abspath(output_filename)))
        df_traj_all.to_csv(OUTPUT_FOLDER + "/" + output_filename, index=False, columns=cols, sep=";")
        del df_traj_all
