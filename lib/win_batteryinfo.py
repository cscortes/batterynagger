def win_battery_info():
    import wmi
    t = wmi.WMI(moniker="//./root/wmi")

    state = "U/K"
    cap = 0
    batts = t.ExecQuery('Select * from BatteryFullChargedCapacity')
    for i, battery in enumerate(batts):
        cap += battery.FullChargedCapacity

    remaining = 0
    batts = t.ExecQuery('Select * from BatteryStatus')
    for i, battery in enumerate(batts):
        print('Charging:          ' + str(battery.Charging))   # need this one
        print('RemainingCapacity: ' + str(battery.RemainingCapacity))

        remaining += battery.RemainingCapacity;

    total_capacity = 100
    if (cap != 0):
        total_capacity = remaining * 100.0 / cap 

    return(int(total_capacity*10)/10, battery.Charging)


if __name__ == "__main__":
    ans = windows_battery_info()
    print(ans)