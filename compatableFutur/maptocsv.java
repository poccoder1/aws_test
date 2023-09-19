import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;

public class CsvConverter {

    public static void mapToCsv(Map<String, Account> map, String csvFilePath) {
        try (FileWriter writer = new FileWriter(csvFilePath)) {
            // Write the CSV header
            writer.append("id,name,type,keyValue");
            writer.append("\n");

            // Iterate through the map and write each Account as a CSV row
            for (Account account : map.values()) {
                writer.append(account.getId()).append(",");
                writer.append(account.getName()).append(",");
                writer.append(account.getType()).append(",");
                writer.append("[");

                // Iterate through the keyValue map and concatenate key-value pairs
                for (Map.Entry<String, String> entry : account.getKeyValue().entrySet()) {
                    writer.append(entry.getKey()).append("=").append(entry.getValue()).append("|");
                }

                // Remove the trailing "|" and close the "keyValue" field
                writer.setLength(writer.length() - 1);
                writer.append("]");

                writer.append("\n");
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}



=====


        import java.io.BufferedReader;
        import java.io.FileReader;
        import java.io.IOException;
        import java.util.HashMap;
        import java.util.Map;
        import java.util.regex.Matcher;
        import java.util.regex.Pattern;

public class CsvConverter {

    public static Map<String, Account> csvToMap(String csvFilePath) {
        Map<String, Account> map = new HashMap<>();

        try (BufferedReader reader = new BufferedReader(new FileReader(csvFilePath))) {
            String line;
            // Skip the header line
            reader.readLine();

            while ((line = reader.readLine()) != null) {
                String[] parts = line.split(",");
                if (parts.length == 4) {
                    String id = parts[0];
                    String name = parts[1];
                    String type = parts[2];
                    String keyValueString = parts[3];

                    // Extract key-value pairs from the keyValueString
                    Map<String, String> keyValue = new HashMap<>();
                    Pattern pattern = Pattern.compile("(\\w+)=(\\w+)");
                    Matcher matcher = pattern.matcher(keyValueString);

                    while (matcher.find()) {
                        keyValue.put(matcher.group(1), matcher.group(2));
                    }

                    // Create an Account object and add it to the map
                    Account account = new Account(id, name, type, keyValue);
                    map.put(id, account);
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return map;
    }
}
