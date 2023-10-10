import pandas as pd
import matplotlib.pyplot as plt
import random

# Створення рандомного набору даних
n = 1000
driver_races = ['Білий', 'Чорний']
stop_dates = [f'2023-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}' for _ in range(n)]
stop_times = [f'{random.randint(0, 23):02d}:{random.randint(0, 59):02d}' for _ in range(n)]
drugs_related_stop = [random.choice([True, False]) for _ in range(n)]
violation_raw = ['Перевищення швидкості', 'Володіння наркотиками', 'Порушення сигналізації', 'Алкогольне сп`яніння', 'Інше']
stop_durations = [f'{random.randint(1, 60)} хв' for _ in range(n)]

data = pd.DataFrame({
    'driver_race': [random.choice(driver_races) for _ in range(n)],
    'stop_date': stop_dates,
    'stop_time': stop_times,
    'drugs_related_stop': drugs_related_stop,
    'violation_raw': [random.choice(violation_raw) for _ in range(n)],
    'stop_duration': stop_durations
})

# Збереження даних у CSV файл
data.to_csv('police_project.csv', index=False)

# Завантаження даних з CSV файлу
data = pd.read_csv('police_project.csv')

# 1. Перевірте, білих чи темношкірих людей частіше зупиняє поліція.
race_counts = data['driver_race'].value_counts()
race_counts.plot(kind='bar')
plt.title('Частота зупинок за расою')
plt.xlabel('Раса')
plt.ylabel('Кількість зупинок')
plt.show()

# 2. З’ясуйте, як часто зупинки через наркотики залежать від часу доби.
data['stop_datetime'] = pd.to_datetime(data['stop_date'] + ' ' + data['stop_time'])
data['hour'] = data['stop_datetime'].dt.hour
drug_stops_by_hour = data[data['drugs_related_stop'] == True]['hour'].value_counts().sort_index()
drug_stops_by_hour.plot(kind='line')
plt.title('Зупинки через наркотики за годинами')
plt.xlabel('Година доби')
plt.ylabel('Кількість зупинок')
plt.show()

# 3. Чи правда, що більшість зупинок водіїв трапляється вночі?
data['stop_datetime'].dt.hour.plot(kind='hist', bins=24, range=(0, 24))
plt.title('Розподіл кількості зупинок за годинами')
plt.xlabel('Година доби')
plt.ylabel('Кількість зупинок')
plt.show()

# 4. Виявіть хибні дані в стовпці 'stop_duration' та замініть їх на NaN.
data['stop_duration'].value_counts()
data['stop_duration'] = data['stop_duration'].replace({'1': '1 min', '2': '2 min', '3': '3 min', '4': '4 min', '5-10': '5-10 min'})
data['stop_duration'] = data['stop_duration'].apply(lambda x: pd.to_numeric(x.split()[0]) if isinstance(x, str) else x)

# 5. Визначте середній час зупинки для кожної з причин зупинки (violation_raw).
mean_stop_duration_by_violation = data.groupby('violation_raw')['stop_duration'].mean()
mean_stop_duration_by_violation.plot(kind='bar', figsize=(10, 6))
plt.title('Середній час зупинки за причиною')
plt.xlabel('Причина зупинки')
plt.ylabel('Середній час зупинки (хв)')
plt.xticks(rotation=90)
plt.show()
