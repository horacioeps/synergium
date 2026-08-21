<?php
/**
 * Plugin Name: Synergium SEO
 * Description: Title, meta description, canonical, hreflang, Open Graph and JSON-LD. No modules.
 * Version: 1.0.1
 * Author: Synergium
 */

if (!defined('ABSPATH')) {
    exit;
}

function synergium_seo_is_es(): bool
{
    if (function_exists('is_page') && is_page('es')) {
        return true;
    }
    $uri = $_SERVER['REQUEST_URI'] ?? '';
    return (bool) preg_match('#^/es(/|$)#', $uri);
}

function synergium_seo_copy(): array
{
    if (synergium_seo_is_es()) {
        return [
            'url'    => 'https://synergium.net/es/',
            'title'  => 'Synergium | Colaboraciones internacionales de investigación',
            'desc'   => 'Identificamos colaboradores internacionales, los contactamos y organizamos las primeras reuniones. Para grupos e instituciones de investigación.',
            'locale' => 'es_ES',
        ];
    }
    return [
        'url'    => 'https://synergium.net/',
        'title'  => 'Synergium | International research collaborations',
        'desc'   => 'We identify international collaborators, contact them and arrange first meetings. For research groups and institutions.',
        'locale' => 'en_US',
    ];
}

add_action('template_redirect', static function () {
    $uri = $_SERVER['REQUEST_URI'] ?? '';
    if (preg_match('#^/en(/|$)#', $uri)) {
        wp_redirect('https://synergium.net/', 301);
        exit;
    }
});

add_filter('pre_get_document_title', static function ($title) {
    if (is_admin()) {
        return $title;
    }
    return synergium_seo_copy()['title'];
});

add_action('wp_head', static function () {
    if (is_admin()) {
        return;
    }
    $c   = synergium_seo_copy();
    $img = 'https://synergium.net/wp-content/uploads/2026/08/synergium-og-1200x630-1.png';
    echo '<meta name="description" content="' . esc_attr($c['desc']) . '" />' . "\n";
    echo '<link rel="canonical" href="' . esc_url($c['url']) . '" />' . "\n";
    echo '<link rel="alternate" hreflang="en" href="https://synergium.net/" />' . "\n";
    echo '<link rel="alternate" hreflang="es" href="https://synergium.net/es/" />' . "\n";
    echo '<link rel="alternate" hreflang="x-default" href="https://synergium.net/" />' . "\n";
    echo '<meta property="og:locale" content="' . esc_attr($c['locale']) . '" />' . "\n";
    echo '<meta property="og:type" content="website" />' . "\n";
    echo '<meta property="og:site_name" content="Synergium" />' . "\n";
    echo '<meta property="og:title" content="' . esc_attr($c['title']) . '" />' . "\n";
    echo '<meta property="og:description" content="' . esc_attr($c['desc']) . '" />' . "\n";
    echo '<meta property="og:url" content="' . esc_url($c['url']) . '" />' . "\n";
    echo '<meta property="og:image" content="' . esc_url($img) . '" />' . "\n";
    echo '<meta property="og:image:width" content="1200" />' . "\n";
    echo '<meta property="og:image:height" content="630" />' . "\n";
    echo '<meta name="twitter:card" content="summary_large_image" />' . "\n";
    echo '<meta name="twitter:title" content="' . esc_attr($c['title']) . '" />' . "\n";
    echo '<meta name="twitter:description" content="' . esc_attr($c['desc']) . '" />' . "\n";
    echo '<meta name="twitter:image" content="' . esc_url($img) . '" />' . "\n";
    $ld = [
        '@context'          => 'https://schema.org',
        '@type'             => 'ProfessionalService',
        'name'              => 'Synergium',
        'url'               => 'https://synergium.net/',
        'email'             => 'info@synergium.net',
        'description'       => $c['desc'],
        'availableLanguage' => ['en', 'es'],
    ];
    echo '<script type="application/ld+json">' . wp_json_encode($ld, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
}, 1);
