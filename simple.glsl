/* simple.glsl */

---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

attribute vec3 v_pos;
attribute vec3 v_normal;
attribute vec2 v_tc0;

uniform mat4 modelview_mat;
uniform mat4 projection_mat;
uniform mat4 normal_mat;

varying vec3 normal_vec;
varying vec4 vertex_pos;
varying vec2 tex_coord;

void main(void) {
    vec4 pos = modelview_mat * vec4(v_pos, 1.0);
    vertex_pos = pos;
    normal_vec = normalize((normal_mat * vec4(v_normal, 0.0)).xyz);
    tex_coord = v_tc0;
    gl_Position = projection_mat * pos;
}

---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

varying vec3 normal_vec;
varying vec4 vertex_pos;
varying vec2 tex_coord;

uniform vec3 diffuse_light;
uniform vec3 ambient_light;
uniform vec3 specular_light;
uniform vec3 diffuse_color;
uniform vec3 ambient_color;
uniform vec3 specular_color;
uniform float shininess;

void main(void) {
    vec3 light_dir = normalize(-vertex_pos.xyz);
    vec3 view_dir = normalize(-vertex_pos.xyz);
    vec3 reflect_dir = reflect(-light_dir, normal_vec);

    // Ambient
    vec3 ambient = ambient_color * ambient_light;

    // Diffuse
    float diff = max(dot(normal_vec, light_dir), 0.0);
    vec3 diffuse = diff * diffuse_color * diffuse_light;

    // Specular
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), shininess);
    vec3 specular = spec * specular_color * specular_light;

    vec3 color = ambient + diffuse + specular;
    gl_FragColor = vec4(color, 1.0);
}
