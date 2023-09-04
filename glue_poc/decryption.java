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


=============bouncycastle


<dependencies>
<!-- Apache POI Core, OOXML, and Encryption Libraries -->
<dependency>
<groupId>org.apache.poi</groupId>
<artifactId>poi</artifactId>
<version>5.0.0</version> <!-- Use the latest version available -->
</dependency>
<dependency>
<groupId>org.apache.poi</groupId>
<artifactId>poi-ooxml</artifactId>
<version>5.0.0</version> <!-- Use the latest version available -->
</dependency>
<dependency>
<groupId>org.bouncycastle</groupId>
<artifactId>bcprov-jdk15on</artifactId>
<version>1.68</version> <!-- Use the latest version available -->
</dependency>
</dependencies>




        import org.apache.poi.ss.usermodel.Workbook;
        import org.apache.poi.ss.usermodel.WorkbookFactory;
        import org.bouncycastle.crypto.CipherParameters;
        import org.bouncycastle.crypto.PBEParametersGenerator;
        import org.bouncycastle.crypto.digests.SHA1Digest;
        import org.bouncycastle.crypto.generators.PKCS12ParametersGenerator;
        import org.bouncycastle.crypto.params.KeyParameter;
        import org.bouncycastle.util.encoders.Base64;

        import java.io.File;
        import java.io.FileInputStream;
        import java.io.FileOutputStream;
        import java.io.IOException;

public class DecryptAndSaveExcel {
    public static void main(String[] args) throws Exception {
        String filePath = "path_to_your_encrypted_file.xlsx";
        String password = "your_password";
        String outputFilePath = "path_to_output_file.xlsx"; // Specify the output file path

        try (FileInputStream fis = new FileInputStream(filePath)) {
            // Decode the Base64-encoded password to get the raw bytes
            byte[] passwordBytes = Base64.decode(password);

            // Generate a secret key using Bouncy Castle
            PBEParametersGenerator generator = new PKCS12ParametersGenerator(new SHA1Digest());
            generator.init(passwordBytes, null, 0);
            CipherParameters params = generator.generateDerivedParameters(128);

            // Load the encrypted workbook with the secret key
            Workbook workbook = WorkbookFactory.create(fis, new KeyParameter(params));

            // Perform any necessary operations on the decrypted workbook here

            // Save the decrypted workbook to the specified output file
            try (FileOutputStream fos = new FileOutputStream(outputFilePath)) {
                workbook.write(fos);
            }

            workbook.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
