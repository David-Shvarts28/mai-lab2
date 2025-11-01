import os
import sys
import tempfile
import shutil
import unittest

class TestShellCommands(unittest.TestCase):
    def setUp(self):
        self.orig_cwd = os.getcwd()

        self.test_dir = tempfile.mkdtemp()
        os.chdir(self.test_dir)

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sys.path.insert(0, project_root)
        sys.path.insert(0, os.path.join(project_root, 'src'))

        if 'src.parser' in sys.modules:
            del sys.modules['src.parser']
        from src.parser import parse
        self.parse = parse

        self.file_test()

    def clean(self):
        os.chdir(self.orig_cwd)
        shutil.rmtree(self.test_dir)

    def file_test(self):
        with open("file_start.txt", "w") as f:
            f.write("AZAZA")

        os.makedirs("dir1")
        os.makedirs("dir2")

        with open("dir1/shell.log", "w") as f:
            f.write("pz")

    def test_ls(self):
        success, result = self.parse("ls")
        self.assertTrue(success)
        self.assertIn("file_start.txt", result)
        self.assertIn("dir1", result)

    def test_ls_empty_dir(self):
        os.makedirs("empty_dir", exist_ok=True)
        success, result = self.parse("ls empty_dir")
        self.assertTrue(success)
        self.assertEqual(result, "")

    def test_ls_with_path(self):
        success, result = self.parse("ls dir1")
        self.assertTrue(success)
        self.assertIn("shell.log", result)

    def test_ls_fake_path(self):
        success, result = self.parse("ls fake_dir")
        self.assertTrue(success)
        self.assertIn("ls: No such file", result)

    def test_ls_detailed(self):
        success, result = self.parse("ls -l")
        self.assertTrue(success)
        self.assertIn("file_start.txt", result)

    def test_cd(self):
        success, result = self.parse("cd dir1")
        self.assertTrue(success)
        self.assertEqual(result, "")
        self.assertTrue(os.getcwd().endswith("dir1"))

    def test_cd_back(self):
        initial_dir = os.getcwd()
        self.parse("cd dir1")
        success, result = self.parse("cd ..")
        self.assertTrue(success)
        self.assertEqual(os.getcwd(), initial_dir)

    def test_cd_home(self):
        success, result = self.parse("cd ~")
        self.assertTrue(success)
        self.assertEqual(result, "")

    def test_cd_no_arguments(self):
        success, result = self.parse("cd")
        self.assertTrue(success)
        self.assertEqual(result, "")

    def test_cd_fake_dir(self):
        initial_cwd = os.getcwd()
        success, result = self.parse("cd fake_dir")
        self.assertTrue(success)
        self.assertIn("cd: No such file", result)
        self.assertEqual(os.getcwd(), initial_cwd)

    def test_cd_file(self):
        success, result = self.parse("cd file_start.txt")
        self.assertTrue(success)
        self.assertIn("cd: Not a directory", result)

    def test_cd_too_many_arguments(self):
        success, result = self.parse("cd a b")
        self.assertTrue(success)
        self.assertIn("too many arguments", result)

    def test_cat_file(self):
        success, result = self.parse("cat file_start.txt")
        self.assertTrue(success)
        self.assertIn("AZAZA", result)
        self.assertIn("", result)

    def test_cat_more_files(self):
        with open("file1.txt", "w") as f:
            f.write("goose")
        with open("file2.txt", "w") as f:
            f.write("patrol")

        success, result = self.parse("cat file1.txt file2.txt")
        self.assertTrue(success)
        self.assertIn("goose", result)
        self.assertIn("patrol", result)

    def test_cat_missing_operand(self):
        success, result = self.parse("cat")
        self.assertTrue(success)
        self.assertEqual(result, "")

    def test_cat_fake_file(self):
        success, result = self.parse("cat fake.txt")
        self.assertTrue(success)
        self.assertIn("cat: fake.txt: No such file", result)

    def test_cat_directory(self):
        success, result = self.parse("cat dir1")
        self.assertTrue(success)
        self.assertIn("cat: dir1: Is a directory", result)

    def test_cp(self):
        success, result = self.parse("cp file_start.txt file_b.txt")
        self.assertTrue(success)
        self.assertTrue(os.path.exists("file_b.txt"))

        with open("file_b.txt", "r") as f:
            content = f.read()
        self.assertIn("AZAZA", content)

    def test_cp_new(self):
        with open("1.txt", "w") as f:
            f.write("1")
        with open("2.txt", "w") as f:
            f.write("2")

        success, result = self.parse("cp 1.txt 2.txt")
        self.assertTrue(success)

        with open("2.txt", "r") as f:
            content = f.read()
        self.assertEqual("1", content)

    def test_cp_r(self):
        success, result = self.parse("cp -r dir1 dir1_copy")
        self.assertTrue(success)
        self.assertTrue(os.path.exists("dir1_copy"))
        self.assertTrue(os.path.exists("dir1_copy/shell.log"))


    def test_mv(self):
        open("1.txt", "w").close()

        success, result = self.parse("mv 1.txt 2.txt")
        self.assertTrue(success)
        self.assertFalse(os.path.exists("1.txt"))
        self.assertTrue(os.path.exists("2.txt"))

    def test_mv_new(self):
        with open("1.txt", "w") as f:
            f.write("1")
        with open("2.txt", "w") as f:
            f.write("2")

        success, result = self.parse("mv 1.txt 2.txt")
        self.assertTrue(success)
        self.assertFalse(os.path.exists("1.txt"))

        with open("2.txt", "r") as f:
            content = f.read()
        self.assertEqual("1", content)

    def test_mv_in_dir(self):
        open("1.txt", "w").close()

        success, result = self.parse("mv 1.txt dir1")
        self.assertTrue(success)
        self.assertFalse(os.path.exists("1.txt"))
        self.assertTrue(os.path.exists("dir1/1.txt"))


    def test_mv_fake_path(self):
        success, result = self.parse("mv fake.txt new.txt")
        self.assertTrue(success)
        self.assertIn("mv: 'fake.txt': No such file", result)


    def test_rm(self):
        success, result = self.parse("rm file_start.txt")
        self.assertTrue(success)
        self.assertFalse(os.path.exists("file_start.txt"))

    def test_rm_more(self):
        open("1.txt", "w").close()
        open("2.txt", "w").close()
        success, result = self.parse("rm 1.txt 2.txt")
        self.assertTrue(success)
        self.assertFalse(os.path.exists("1.txt"))
        self.assertFalse(os.path.exists("2.txt"))

    def test_rm_no_r(self):
        success, result = self.parse("rm dir1")
        self.assertTrue(success)
        self.assertIn("rm: cannot remove 'dir1': Is a directory", result)

    def test_zip(self):
        success, result = self.parse("zip dir1 archive.zip")
        self.assertTrue(success)
        self.assertTrue(os.path.exists("archive.zip"))

    def test_tar(self):
        success, result = self.parse("tar dir1 archive.tar.gz")
        self.assertTrue(success)
        self.assertTrue(os.path.exists("archive.tar.gz"))



    def test_grep_simple(self):
        success, result = self.parse("grep AZAZA file_start.txt")
        self.assertTrue(success)
        self.assertIn("AZAZA", result)





    def test_grep_invalid(self):
        success, result = self.parse("grep '[' file_start.txt")
        self.assertTrue(success)
        self.assertIn("invalid pattern", result)


    def test_history_limit(self):
        for i in range(5):
            self.parse(f"echo command{i}")

        success, result = self.parse("history 3")
        self.assertTrue(success)

    def test_history_args(self):
        success, result = self.parse("history 0")
        self.assertTrue(success)
        self.assertIn("argument must be greater than 0", result)

        success, result = self.parse("history x")
        self.assertTrue(success)
        self.assertIn("numeric argument required", result)

        success, result = self.parse("history 1 2")
        self.assertTrue(success)
        self.assertIn("too many arguments", result)

    def test_unknown_command(self):
        success, result = self.parse("unknown_command")
        self.assertFalse(success)
        self.assertIn("не найдена", result)

    def test_empty_command(self):
        success, result = self.parse("")
        self.assertTrue(success)
        self.assertEqual(result, "")





if __name__ == '__main__':
    unittest.main()
