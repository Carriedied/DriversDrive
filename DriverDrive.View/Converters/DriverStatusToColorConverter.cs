using System.Globalization;
using System.Windows.Data;
using System.Windows.Media;

namespace DriverDrive.View.Converters
{
    public class DriverStatusToColorConverter : IValueConverter
    {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
        {
            if (value is Core.Models.DriverStatus status)
            {
                return status switch
                {
                    Core.Models.DriverStatus.Missing => new SolidColorBrush(Colors.Red),
                    Core.Models.DriverStatus.Outdated => new SolidColorBrush(Colors.Orange),
                    Core.Models.DriverStatus.UpToDate => new SolidColorBrush(Colors.Green),
                    _ => new SolidColorBrush(Colors.Gray)
                };
            }

            return new SolidColorBrush(Colors.Gray);
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        {
            throw new NotImplementedException();
        }
    }
}
