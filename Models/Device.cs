using DriversDrivers.Common;

namespace DriversDrivers.Models
{
    public class Device : ObservableObject
    {
        private string _name;
        private DriverStatus _driverStatus;
        private string _driverUrl;

        public string Name
        {
            get => _name;
            set => SetProperty(ref _name, value);
        }

        public DriverStatus DriverStatus
        {
            get => _driverStatus;
            set => SetProperty(ref _driverStatus, value);
        }

        public string DriverUrl
        {
            get => _driverUrl;
            set => SetProperty(ref _driverUrl, value);
        }
    }
}
