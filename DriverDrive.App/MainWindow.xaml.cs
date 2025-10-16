using DriverDrive.ViewModel;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace DriverDrive.App
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        public MainWindow(MainViewModel viewModel)
        {
            Console.WriteLine($"MainWindow constructor called with ViewModel: {viewModel?.GetType().Name}");
            InitializeComponent();

            DataContext = viewModel;

            Console.WriteLine($"MainWindow created with ViewModel: {viewModel?.GetType().Name}");
            Console.WriteLine($"DataContext set to: {DataContext?.GetType().Name}");
        }
    }
}