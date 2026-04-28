from MailAddress import MailAddress as MailAddress
import unittest


class TestMailAddress(unittest.TestCase):

    # ----- TRUE Tests - Local Part -----
    def test_local_part_standard_alpha_num(self):
        self.assertTrue(MailAddress._isValidLocalPart('MohammadWang123'))

    def test_local_part_single_char(self):
        self.assertTrue(MailAddress._isValidLocalPart('M'))
        self.assertTrue(MailAddress._isValidLocalPart('m'))
        self.assertTrue(MailAddress._isValidLocalPart('1'))

    def test_local_part_standard_dot(self):
        self.assertTrue(MailAddress._isValidLocalPart('Mohammad.Wang'))

    def test_local_part_common_alias(self):
        self.assertTrue(MailAddress._isValidLocalPart("Mohammad+Wang"))

    def test_local_part_hyphens(self):
        self.assertTrue(MailAddress._isValidLocalPart('Mohammad-Wang'))
        self.assertTrue(MailAddress._isValidLocalPart('-Mohammad-Wang-'))


    # ----- FALSE Tests - Local Part -----
    def test_local_part_empty_string(self):
        self.assertFalse(MailAddress._isValidLocalPart(""))

    def test_local_part_trailing_dot(self):
        self.assertFalse(MailAddress._isValidLocalPart("MohammadWang."))

    def test_local_part_consecutive_dots(self):
        self.assertFalse(MailAddress._isValidLocalPart("Mohammad..Wang"))

    def test_local_part_multiple_consecutive_dots(self):
        self.assertFalse(MailAddress._isValidLocalPart("Mohammad...Wang"))

    def test_local_part_invalid_character_space(self):
        self.assertFalse(MailAddress._isValidLocalPart("Mohammad Wang"))

    def test_local_part_invalid_character_quotes(self):
        self.assertFalse(MailAddress._isValidLocalPart('"MohammadWang"'))

    def test_local_part_invalid_character_brackets(self):
        self.assertFalse(MailAddress._isValidLocalPart('Mohammad[Wang]'))
        self.assertFalse(MailAddress._isValidLocalPart('Mohammad(Wang)'))
        self.assertFalse(MailAddress._isValidLocalPart('Mohammad<Wang>'))

    # ----- True Test - Domain -----

    def test_domain_standard_domain(self):
        self.assertTrue(MailAddress._isValidDomainSyntax('example.com'))
        self.assertTrue(MailAddress._isValidDomainSyntax('example.org'))
        self.assertTrue(MailAddress._isValidDomainSyntax('example.net'))
        self.assertTrue(MailAddress._isValidDomainSyntax('example.io'))
        self.assertTrue(MailAddress._isValidDomainSyntax('example.gov'))

    def test_domain_subdomains(self):
        self.assertTrue(MailAddress._isValidDomainSyntax('sub.mail.example.com'))

    def test_domain_hyphenated(self):
        self.assertTrue(MailAddress._isValidDomainSyntax('my-custom-domain.org'))

    def test_domain_numeric(self):
        self.assertTrue(MailAddress._isValidDomainSyntax('123.com'))

    def test_domain_single_character(self):
        self.assertTrue(('a.com'))

    # ----- FALSE Tests - Domain -----

    def test_domain_empty(self):
        self.assertFalse(MailAddress._isValidDomainSyntax(''))

    def test_domain_leading_hyphen(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('-example.com'))

    def test_domain_trailing_hyphen(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('example-.com'))

    def test_domain_top_level_domain_hyphen(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('example.-org'))
        self.assertFalse(MailAddress._isValidDomainSyntax('example.-com'))

    def test_domain_top_level_domain_numeric(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('example.123'))

    def test_domain_all_numeric(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('12345'))

    def test_domain_consecutive_dots(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('example..com'))

    def test_domain_leading_dot(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('.example.com'))

    def test_domain_trailing_dot(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('example.com.'))

    def test_domain_invalid_characters(self):
        self.assertFalse(MailAddress._isValidDomainSyntax('example_domain.com'))
        self.assertFalse(MailAddress._isValidDomainSyntax('example domain.com'))


if __name__ == '__main__':
    unittest.main()