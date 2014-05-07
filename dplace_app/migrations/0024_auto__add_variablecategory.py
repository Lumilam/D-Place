# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VariableCategory'
        db.create_table(u'dplace_app_variablecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
        ))
        db.send_create_signal(u'dplace_app', ['VariableCategory'])

        # Adding M2M table for field index_categories on 'VariableDescription'
        m2m_table_name = db.shorten_name(u'dplace_app_variabledescription_index_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('variabledescription', models.ForeignKey(orm[u'dplace_app.variabledescription'], null=False)),
            ('variablecategory', models.ForeignKey(orm[u'dplace_app.variablecategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['variabledescription_id', 'variablecategory_id'])

        # Adding M2M table for field niche_categories on 'VariableDescription'
        m2m_table_name = db.shorten_name(u'dplace_app_variabledescription_niche_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('variabledescription', models.ForeignKey(orm[u'dplace_app.variabledescription'], null=False)),
            ('variablecategory', models.ForeignKey(orm[u'dplace_app.variablecategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['variabledescription_id', 'variablecategory_id'])


    def backwards(self, orm):
        # Deleting model 'VariableCategory'
        db.delete_table(u'dplace_app_variablecategory')

        # Removing M2M table for field index_categories on 'VariableDescription'
        db.delete_table(db.shorten_name(u'dplace_app_variabledescription_index_categories'))

        # Removing M2M table for field niche_categories on 'VariableDescription'
        db.delete_table(db.shorten_name(u'dplace_app_variabledescription_niche_categories'))


    models = {
        u'dplace_app.environmental': {
            'Meta': {'object_name': 'Environmental'},
            'actual_location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'amphibian_diversity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'annual_mean_precipitation': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'annual_mean_temperature': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'annual_precipitation_variance': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'annual_temperature_variance': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'bird_diversity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'elevation': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'environmentals'", 'null': 'True', 'to': u"orm['dplace_app.ISOCode']"}),
            'mammal_diversity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'mean_growing_season_duration': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'net_primary_productivity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'plant_diversity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'precipitation_constancy': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'precipitation_contingency': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'precipitation_predictability': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'reported_location': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'slope': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'society': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'environmentals'", 'null': 'True', 'to': u"orm['dplace_app.Society']"}),
            'temperature_constancy': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'temperature_contingency': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'temperature_predictability': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'dplace_app.isocode': {
            'Meta': {'object_name': 'ISOCode'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'db_index': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'})
        },
        u'dplace_app.language': {
            'Meta': {'object_name': 'Language'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'languages'", 'unique': 'True', 'to': u"orm['dplace_app.ISOCode']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'})
        },
        u'dplace_app.languageclass': {
            'Meta': {'ordering': "('level', 'name')", 'object_name': 'LanguageClass'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['dplace_app.LanguageClass']", 'null': 'True'})
        },
        u'dplace_app.languageclassification': {
            'Meta': {'object_name': 'LanguageClassification', 'index_together': "[['class_family', 'class_subfamily', 'class_subsubfamily']]"},
            'class_family': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'languages1'", 'null': 'True', 'to': u"orm['dplace_app.LanguageClass']"}),
            'class_subfamily': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'languages2'", 'null': 'True', 'to': u"orm['dplace_app.LanguageClass']"}),
            'class_subsubfamily': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'languages3'", 'null': 'True', 'to': u"orm['dplace_app.LanguageClass']"}),
            'ethnologue_classification': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dplace_app.Language']", 'null': 'True'}),
            'scheme': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'})
        },
        u'dplace_app.society': {
            'Meta': {'object_name': 'Society'},
            'ext_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'societies'", 'null': 'True', 'to': u"orm['dplace_app.ISOCode']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'societies'", 'null': 'True', 'to': u"orm['dplace_app.Language']"}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        u'dplace_app.source': {
            'Meta': {'unique_together': "(('year', 'author'),)", 'object_name': 'Source'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'focal_year': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'subcase': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'dplace_app.variablecategory': {
            'Meta': {'object_name': 'VariableCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        },
        u'dplace_app.variablecodedescription': {
            'Meta': {'ordering': "('variable', 'code_number', 'code')", 'object_name': 'VariableCodeDescription'},
            'code': ('django.db.models.fields.CharField', [], {'default': "'.'", 'max_length': '20', 'db_index': 'True'}),
            'code_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'codes'", 'to': u"orm['dplace_app.VariableDescription']"})
        },
        u'dplace_app.variablecodedvalue': {
            'Meta': {'ordering': "('variable', 'coded_value')", 'unique_together': "(('variable', 'society', 'coded_value'),)", 'object_name': 'VariableCodedValue', 'index_together': "[['variable', 'society'], ['variable', 'coded_value'], ['variable', 'code'], ['society', 'coded_value'], ['society', 'code']]"},
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dplace_app.VariableCodeDescription']", 'null': 'True'}),
            'coded_value': ('django.db.models.fields.CharField', [], {'default': "'.'", 'max_length': '20', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'society': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dplace_app.Society']", 'null': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dplace_app.Source']", 'null': 'True'}),
            'variable': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'values'", 'to': u"orm['dplace_app.VariableDescription']"})
        },
        u'dplace_app.variabledescription': {
            'Meta': {'ordering': "('label',)", 'object_name': 'VariableDescription'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'index_variables'", 'symmetrical': 'False', 'to': u"orm['dplace_app.VariableCategory']"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '200', 'db_index': 'True'}),
            'niche_categories': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'niche_variables'", 'symmetrical': 'False', 'to': u"orm['dplace_app.VariableCategory']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dplace_app.Source']", 'null': 'True'})
        }
    }

    complete_apps = ['dplace_app']