import org.apache.poi.poifs.crypt.Decryptor;
import org.apache.poi.poifs.filesystem.POIFSFileSystem;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;

public class DecryptXLS {
    public static void main(String[] args) throws Exception {
        String filePath = "path_to_your_encrypted_file.xlsx";
        String password = "your_password";
        String outputFilePath = "path_to_output_file.xlsx"; // Specify the output file path

        POIFSFileSystem fs = new POIFSFileSystem(new FileInputStream(filePath));
        Decryptor decryptor = Decryptor.getInstance();
        decryptor.verifyPassword(password);
        InputStream dataStream = decryptor.getDataStream(fs);

        Workbook workbook = new XSSFWorkbook(dataStream);

        // Perform any necessary operations on the decrypted workbook here

        // Save the decrypted workbook to the specified output file
        try (OutputStream out = new FileOutputStream(outputFilePath)) {
            workbook.write(out);
        }

        workbook.close();
    }
}


=====RC4

        import org.apache.poi.poifs.crypt.Decryptor;
        import org.apache.poi.poifs.filesystem.POIFSFileSystem;
        import org.apache.poi.ss.usermodel.Workbook;
        import org.apache.poi.xssf.usermodel.XSSFWorkbook;

        import java.io.File;
        import java.io.FileInputStream;
        import java.io.FileOutputStream;
        import java.io.InputStream;
        import java.io.OutputStream;

public class DecryptAndSaveXLS {
    public static void main(String[] args) throws Exception {
        String filePath = "path_to_your_encrypted_file.xlsx";
        String password = "your_password";
        String outputFilePath = "path_to_output_file.xlsx"; // Specify the output file path

        POIFSFileSystem fs = new POIFSFileSystem(new FileInputStream(filePath));
        Decryptor decryptor = Decryptor.getInstance();
        decryptor.verifyPassword(password);
        InputStream dataStream = decryptor.getDataStream(fs);

        Workbook workbook = new XSSFWorkbook(dataStream);

        // Perform any necessary operations on the decrypted workbook here

        // Save the decrypted workbook to the specified output file
        try (OutputStream out = new FileOutputStream(outputFilePath)) {
            workbook.write(out);
        }

        workbook.close();
    }
}


=====AES Encryption

        import org.apache.poi.poifs.crypt.Decryptor;
        import org.apache.poi.poifs.filesystem.POIFSFileSystem;
        import org.apache.poi.ss.usermodel.Workbook;
        import org.apache.poi.xssf.usermodel.XSSFWorkbook;

        import java.io.File;
        import java.io.FileInputStream;
        import java.io.FileOutputStream;
        import java.io.InputStream;
        import java.io.OutputStream;

public class DecryptAndSaveXLS {
    public static void main(String[] args) throws Exception {
        String filePath = "path_to_your_encrypted_file.xlsx";
        String password = "your_password";
        String outputFilePath = "path_to_output_file.xlsx"; // Specify the output file path

        POIFSFileSystem fs = new POIFSFileSystem(new FileInputStream(filePath));
        Decryptor decryptor = Decryptor.getInstance();
        decryptor.verifyPassword(password);
        InputStream dataStream = decryptor.getDataStream(fs);

        Workbook workbook = new XSSFWorkbook(dataStream);

        // Perform any necessary operations on the decrypted workbook here

        // Save the decrypted workbook to the specified output file
        try (OutputStream out = new FileOutputStream(outputFilePath)) {
            workbook.write(out);
        }

        workbook.close();
    }
}
