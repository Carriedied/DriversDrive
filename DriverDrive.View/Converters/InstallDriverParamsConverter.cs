using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Data;

namespace DriverDrive.View.Converters
{
    public class InstallDriverParamsConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            var device = parameter as Core.Models.Device;
            var viewModel = value as ViewModel.MainViewModel;

            return new object[] { device, "192.168.1.10" };
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
