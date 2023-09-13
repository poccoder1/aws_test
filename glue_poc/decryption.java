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
======



        I hope this email finds you well. I am writing to bring to your attention an issue we have been facing with decrypting the files you've shared with us recently. It appears that there may have been a change in your encryption logic after September 6th.

        We have been successfully decrypting files that were shared with us prior to that date using the previous encryption method. However, this same method is no longer working for the new files you've sent us.

        To resolve this matter promptly, I kindly request that you liaise with your IT team to investigate the issue and potentially revert to the encryption process we were using before September 6th. If there have been any updates or changes to the encryption method, we would appreciate receiving the necessary information or files to ensure successful decryption.

        Alternatively, if you believe it would be more expedient, we are open to scheduling a call with your IT team to address this matter directly. This would allow us to collaborate and find a solution as quickly as possible, minimizing any disruption to our workflow.

        Please let us know how you would like to proceed, and we are committed to working together to resolve this issue swiftly. Your prompt attention to this matter is greatly appreciated.

        Thank you for your cooperation.

=================

        Subject: Re: Issue with Encryption Method for Files Shared after September 6th

        Dear [Sender's Name],

        Thank you for getting back to us promptly, and I appreciate your understanding of the urgency of this matter. I want to clarify that the issue we're experiencing with file decryption does not appear to be related to the password length; rather, it seems to be connected to a change in the encryption method used by your IT team after September 6th.

        To resolve this issue, I believe it's crucial to identify the encryption algorithm that was employed prior to September 6th, as our existing decryption method is no longer compatible. If you could kindly liaise with your IT team to retrieve this information, it would be greatly appreciated.

        Moreover, we are more than willing to collaborate with your IT team to ensure a smooth resolution. If they require any specific inputs or details from our end, please let us know, and we will promptly provide the necessary information. Setting up a call to discuss this matter in detail would be a constructive step towards finding a solution as quickly as possible, and we are open to this option.

        The current situation is impacting our workflow and causing delays in processing the files, as we are forced to handle them manually. We understand the importance of resolving this issue swiftly, and we are committed to working closely with you to achieve that goal.

        Once again, thank you for your assistance in addressing this matter. Please do not hesitate to reach out with any further information or to arrange a suitable time for a call with your IT team.

        Best regards,

        [Your Name]
        [Your Position]
        [Your Contact Information]