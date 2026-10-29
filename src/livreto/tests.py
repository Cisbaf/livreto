from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Livreto


@override_settings(ALLOWED_HOSTS=["testserver"])
class LivretoAccessTests(TestCase):
    def setUp(self):
        self.livreto = Livreto.objects.create(name="Edição 1", system="observatorio", pdf="livretos/x.pdf")
        self.user = get_user_model().objects.create_user("admin", password="s3nha-forte-123")

    def test_rotas_de_gestao_exigem_login(self):
        urls = [
            reverse("livreto_index"),
            reverse("livreto_register"),
            reverse("livreto_update", args=[self.livreto.pk]),
            reverse("livreto_delete", args=[self.livreto.pk]),
        ]
        for url in urls:
            for method in ("get", "post"):
                resp = getattr(self.client, method)(url)
                self.assertEqual(resp.status_code, 302, f"{method} {url}")
                self.assertIn(reverse("login"), resp["Location"], f"{method} {url}")
        self.assertTrue(Livreto.objects.filter(pk=self.livreto.pk).exists())

    def test_delete_por_get_nao_apaga_nem_logado(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("livreto_delete", args=[self.livreto.pk]))
        self.assertEqual(resp.status_code, 405)
        self.assertTrue(Livreto.objects.filter(pk=self.livreto.pk).exists())

    def test_delete_por_post_logado_apaga(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse("livreto_delete", args=[self.livreto.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Livreto.objects.filter(pk=self.livreto.pk).exists())

    def test_delete_sem_csrf_e_rejeitado(self):
        from django.test import Client
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        resp = client.post(reverse("livreto_delete", args=[self.livreto.pk]))
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(Livreto.objects.filter(pk=self.livreto.pk).exists())

    def test_login_funciona_e_redireciona_para_o_index(self):
        resp = self.client.post(reverse("login"), {"username": "admin", "password": "s3nha-forte-123"})
        self.assertRedirects(resp, reverse("livreto_index"), fetch_redirect_response=False)
        self.assertEqual(self.client.get(reverse("livreto_index")).status_code, 200)

    def test_login_com_senha_errada_nao_autentica(self):
        resp = self.client.post(reverse("login"), {"username": "admin", "password": "errada"})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.client.get(reverse("livreto_index")).status_code, 302)

    def test_endpoints_publicos_continuam_abertos(self):
        self.assertEqual(self.client.get(reverse("livreto_infos", args=["observatorio"])).status_code, 200)
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)
