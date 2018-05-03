using System;
using System.IO;
using System.Text;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.Linq;

namespace TestePygtail
{
    class Program
    {
        static void Main(string[] args)
        {
            
            string[] lines = File.ReadAllLines(@"/var/log/auth.log");

            // Display the file contents by using a foreach loop.
            string startXML = "<?xml version=\"1.0\" encoding=\"UTF - 8\"?><message><host name=\"fqdn\" ip =\"127.0.0.1\"/>< report date = \"2017-08-21T17:00:01.000001\" ><payload>";
            Console.WriteLine("<?xml version=\"1.0\" encoding=\"UTF - 8\"?><message><host name=\"fqdn\" ip =\"127.0.0.1\"/>< report date = \"2017-08-21T17:00:01.000001\" ><payload>");

            foreach (string line in lines)
            {
                if (line.Contains("sshd"))
                {
                    if (line.Contains("Accepted"))
                    {
                        string[] teste = line.Split();

                        string entryService = line.Substring(0, 15);
                        string user = (line.Split()[8]);
                        string ip_addres = (line.Split()[10]);
                        string connect_date = "";
                        string access = line.Split()[5];

                        startXML += "<entry service = " + entryService + " user = " + user + " ip_addres = " + ip_addres + " connect_date = " + connect_date + " access = " + access + " />";
                        Console.WriteLine("<entry service = " + entryService + " user = " + user + " ip_addres = " + ip_addres + " connect_date = " + connect_date + " access = " + access + " />");

                    }
                }                
            }

            startXML += "</payload></message>";
            Console.WriteLine("</payload ></message>");            
            
            Console.WriteLine("Pressione qualquer tecla para fazer o download do xml");
            Console.ReadKey();
            File.WriteAllText(@"C:\temp\testexml.xml", startXML);

            Console.WriteLine("Press any key to exit.");
            Console.ReadKey();
        }
    }
}
