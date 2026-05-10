from mail_exchange import MailAddress as MailAddress, MailServer
import unittest


class TestMailAddress(unittest.TestCase):

    # ----- TRUE Tests - Local Part -----
    def test_local_part_standard_alpha_num(self):
        """Testing local part with standard alphanumeric characters should return True.
        """
        self.assertTrue(MailAddress._is_valid_local_part('MohammadWang123'))

    def test_local_part_single_char(self):
        """Testing local part with a single character should return True.
        """
        self.assertTrue(MailAddress._is_valid_local_part('M'))
        self.assertTrue(MailAddress._is_valid_local_part('m'))
        self.assertTrue(MailAddress._is_valid_local_part('1'))

    def test_local_part_standard_dot(self):
        """Testing local part with standard dot usage should return True.
        """
        self.assertTrue(MailAddress._is_valid_local_part('Mohammad.Wang'))

    def test_local_part_common_alias(self):
        """Testing local part with common alias syntax should return True.
        """
        self.assertTrue(MailAddress._is_valid_local_part("Mohammad+Wang"))

    def test_local_part_hyphens(self):
        """Testing local part with hyphens should return True.
        """
        self.assertTrue(MailAddress._is_valid_local_part('Mohammad-Wang'))
        self.assertTrue(MailAddress._is_valid_local_part('-Mohammad-Wang-'))


    # ----- FALSE Tests - Local Part -----
    def test_local_part_empty_string(self):
        """Testing local part with an empty string should return False.
        """
        self.assertFalse(MailAddress._is_valid_local_part(""))

    def test_local_part_trailing_dot(self):
        """Testing local part with a trailing dot should return False.
        """
        self.assertFalse(MailAddress._is_valid_local_part("MohammadWang."))

    def test_local_part_consecutive_dots(self):
        """Testing local part with consecutive dots should return False.
        """
        self.assertFalse(MailAddress._is_valid_local_part("Mohammad..Wang"))

    def test_local_part_multiple_consecutive_dots(self):
        """Testing local part with multiple consecutive dots should return False.
        """
        self.assertFalse(MailAddress._is_valid_local_part("Mohammad...Wang"))

    def test_local_part_invalid_character_space(self):
        """Testing local part with invalid character (space) should return False.
        """
        self.assertFalse(MailAddress._is_valid_local_part("Mohammad Wang"))

    def test_local_part_invalid_character_quotes(self):
        """Testing local part with invalid character (quotes) should return False.
        """
        self.assertFalse(MailAddress._is_valid_local_part('"MohammadWang"'))

    def test_local_part_invalid_character_brackets(self):
        """Testing local part with invalid characters (brackets) should return False.
        """
        self.assertFalse(MailAddress._is_valid_local_part('Mohammad[Wang]'))
        self.assertFalse(MailAddress._is_valid_local_part('Mohammad(Wang)'))
        self.assertFalse(MailAddress._is_valid_local_part('Mohammad<Wang>'))

    # ----- True Test - Domain -----

    def test_domain_standard_domain(self):
        """Testing domain with standard syntax should return True.
        """
        self.assertTrue(MailServer._is_resolvable_domain('example.com'))
        self.assertTrue(MailServer._is_resolvable_domain('example.org'))
        self.assertTrue(MailServer._is_resolvable_domain('example.net'))
        self.assertTrue(MailServer._is_resolvable_domain('example.io'))
        self.assertTrue(MailServer._is_resolvable_domain('example.gov'))

    def test_domain_subdomains(self):
        """Testing domain with subdomains should return True.
        """
        self.assertTrue(MailServer._is_resolvable_domain('sub.mail.example.com'))

    def test_domain_hyphenated(self):
        """Testing domain with hyphens should return True.
        """
        self.assertTrue(MailServer._is_resolvable_domain('my-custom-domain.org'))

    def test_domain_numeric(self):
        """Testing domain with numeric characters should return True.
        """
        self.assertTrue(MailServer._is_resolvable_domain('example123.com'))
        self.assertTrue(MailServer._is_resolvable_domain('123.com'))

    def test_domain_single_character(self):
        """Testing domain with single character should return True.
        """
        self.assertTrue(MailServer._is_resolvable_domain('a.com'))

    # ----- FALSE Tests - Domain -----

    def test_domain_empty(self):
        """Testing empty domain should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain(''))

    def test_domain_leading_hyphen(self):
        self.assertFalse(MailServer._is_resolvable_domain('-example.com'))

    def test_domain_trailing_hyphen(self):
        """Testing domain with trailing hyphen should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('example-.com'))

    def test_domain_top_level_domain_hyphen(self):
        """Testing domain with hyphen in top-level domain should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('example.-org'))
        self.assertFalse(MailServer._is_resolvable_domain('example.-com'))

    def test_domain_top_level_domain_numeric(self):
        """Testing domain with numeric characters in top-level domain should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('example.123'))

    def test_domain_all_numeric(self):
        """Testing domain with all numeric characters should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('12345'))

    def test_domain_consecutive_dots(self):
        """Testing domain with consecutive dots should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('example..com'))

    def test_domain_leading_dot(self):
        """Testing domain with leading dot should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('.example.com'))

    def test_domain_trailing_dot(self):
        """Testing domain with trailing dot should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('example.com.'))

    def test_domain_invalid_characters(self):
        """Testing domain with invalid characters should return False.
        """
        self.assertFalse(MailServer._is_resolvable_domain('example_domain.com'))
        self.assertFalse(MailServer._is_resolvable_domain('example domain.com'))

if __name__ == '__main__':
    unittest.main()